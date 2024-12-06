import sqlite3
from datetime import datetime
from typing import List, Tuple
from pathlib import Path

DB_NAME = Path("~/.gradebook/gradebook.db").expanduser()
if not DB_NAME.exists():
    DB_NAME.mkdir(parents=True, exist_ok=True)

class GradeBookError(Exception):
    """Custom exception for Gradebook errors"""
    pass


class Gradebook:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        # Courses table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            semester TEXT
        )
        ''')

        # Categories table for assignment weights
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            category_name TEXT NOT NULL,
            weight REAL NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            UNIQUE(course_id, category_name)
        )
        ''')

        # Assignments table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            category_id INTEGER,
            title TEXT NOT NULL,
            max_points REAL NOT NULL,
            earned_points REAL NOT NULL,
            entry_date TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
        ''')

        self.conn.commit()

    def validate_category_weights(self, course_id: int, new_category_weight: float = 0) -> bool:
        """
        Validate that all category weights for a course sum to 1.0 (100%).
        """
        self.cursor.execute('''
        SELECT SUM(weight) FROM categories WHERE course_id = ?
        ''', (course_id,))
        current_sum = self.cursor.fetchone()[0] or 0
        total_sum = current_sum + new_category_weight

        # Allow sums that are exactly 1.0 or very close to it
        tolerance = 0.0001
        return abs(total_sum - 1.0) <= tolerance

    def get_remaining_weight(self, course_id: int) -> float:
        """Calculate remaining weight available for new categories."""
        self.cursor.execute('''
        SELECT SUM(weight) FROM categories WHERE course_id = ?
        ''', (course_id,))
        current_sum = self.cursor.fetchone()[0] or 0
        return max(0.0, round(1.0 - current_sum, 4))

    def add_category(self, course_id: int, category_name: str, weight: float) -> int:
        """Add a new category for a course."""
        remaining_weight = self.get_remaining_weight(course_id)
        tolerance = 0.0001

        # Allow weights that are equal to or very close to the remaining weight
        if weight > remaining_weight + tolerance:
            raise GradeBookError(
                f"Invalid weight {weight}. Remaining weight available: {remaining_weight} (tolerance: ±{tolerance})"
            )

        try:
            self.cursor.execute('''
            INSERT INTO categories (course_id, category_name, weight)
            VALUES (?, ?, ?)
            ''', (course_id, category_name, weight))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            raise GradeBookError(f"Category '{category_name}' already exists for this course")

    def add_categories(self, course_id: int, categories: List[Tuple[str, float]]):
        """Add multiple categories for a course at once."""
        total_weight = sum(weight for _, weight in categories)
        tolerance = 0.0001

        if not abs(total_weight - 1.0) <= tolerance:  # Allow exact 100% with tolerance
            raise GradeBookError(
                f"Category weights must sum to 100% (got {total_weight * 100:.2f}%, tolerance: ±{tolerance * 100:.2f}%)"
            )

        try:
            for category_name, weight in categories:
                self.cursor.execute('''
                INSERT INTO categories (course_id, category_name, weight)
                VALUES (?, ?, ?)
                ''', (course_id, category_name, weight))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise GradeBookError("Duplicate category names are not allowed")

    def ensure_unassigned_category(self, course_id: int) -> int:
        """
        Ensure an 'Unassigned' category exists for the course and return its ID.
        Creates with zero weight if it doesn't exist.
        """
        self.cursor.execute('''
        SELECT category_id FROM categories 
        WHERE course_id = ? AND category_name = 'Unassigned'
        ''', (course_id,))
        result = self.cursor.fetchone()

        if result:
            return result[0]

        # Create new Unassigned category with 0 weight
        self.cursor.execute('''
        INSERT INTO categories (course_id, category_name, weight)
        VALUES (?, 'Unassigned', 0.0)
        ''', (course_id,))
        self.conn.commit()
        return self.cursor.lastrowid

    def remove_category(self, category_id: int, preserve_assignments: bool = True) -> tuple[str, int]:
        """
        Remove a category, optionally preserving its assignments.

        Args:
            category_id: The ID of the category to remove
            preserve_assignments: If True, move assignments to Unassigned category
                                If False, delete assignments

        Returns:
            Tuple of (category_name, number_of_assignments_affected)
        """
        # Get category details and course_id
        self.cursor.execute('''
        SELECT category_name, course_id, 
               (SELECT COUNT(*) FROM assignments WHERE category_id = ?) as assignment_count
        FROM categories 
        WHERE category_id = ?
        ''', (category_id, category_id))

        result = self.cursor.fetchone()
        if not result:
            raise GradeBookError("Category not found")

        category_name, course_id, assignment_count = result

        # Don't allow removing the Unassigned category
        if category_name == 'Unassigned':
            raise GradeBookError("Cannot remove the Unassigned category")

        if preserve_assignments and assignment_count > 0:
            # Get or create Unassigned category
            unassigned_id = self.ensure_unassigned_category(course_id)

            # Move assignments to Unassigned category
            self.cursor.execute('''
            UPDATE assignments 
            SET category_id = ? 
            WHERE category_id = ?
            ''', (unassigned_id, category_id))

        # Remove the category
        self.cursor.execute('DELETE FROM categories WHERE category_id = ?', (category_id,))
        self.conn.commit()

        return category_name, assignment_count

    def update_category_weight(self, category_id: int, new_weight: float):
        """Update the weight of a category."""
        # Get course_id for the category
        self.cursor.execute('''
        SELECT course_id FROM categories WHERE category_id = ?
        ''', (category_id,))
        result = self.cursor.fetchone()
        if not result:
            raise GradeBookError("Category not found")

        course_id = result[0]

        # Get current weight
        self.cursor.execute('''
        SELECT weight FROM categories WHERE category_id = ?
        ''', (category_id,))
        current_weight = self.cursor.fetchone()[0]

        # Calculate the remaining weight
        remaining_weight = self.get_remaining_weight(course_id) + current_weight
        tolerance = 0.0001

        if new_weight > remaining_weight + tolerance:
            raise GradeBookError(
                f"New weight would exceed 100%. Maximum allowed: {remaining_weight} (tolerance: ±{tolerance})"
            )

        self.cursor.execute('''
        UPDATE categories SET weight = ? WHERE category_id = ?
        ''', (new_weight, category_id))
        self.conn.commit()

    def add_course(self, course_name: str, semester: str) -> int:
        """Add a new course to the database."""
        self.cursor.execute('''
        INSERT INTO courses (course_name, semester)
        VALUES (?, ?)
        ''', (course_name, semester))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_assignment(self, course_id: int, category_id: int, title: str,
                       max_points: float, earned_points: float) -> int:
        """Add a new assignment."""
        # Verify category belongs to course
        self.cursor.execute('''
        SELECT COUNT(*) FROM categories 
        WHERE category_id = ? AND course_id = ?
        ''', (category_id, course_id))
        if self.cursor.fetchone()[0] == 0:
            raise GradeBookError("Category does not belong to this course")

        entry_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
        INSERT INTO assignments (course_id, category_id, title, max_points, earned_points, entry_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (course_id, category_id, title, max_points, earned_points, entry_date))
        self.conn.commit()
        return self.cursor.lastrowid

    def calculate_course_grade(self, course_id: int) -> float:
        """Calculate the overall weighted grade for a course."""
        if not self.validate_category_weights(course_id):
            raise GradeBookError("Category weights do not sum to 100%")

        # Get all categories for the course
        self.cursor.execute('''
        SELECT category_id, weight 
        FROM categories 
        WHERE course_id = ?
        ''', (course_id,))
        categories = self.cursor.fetchall()

        total_weighted_grade = 0
        total_weight_used = 0

        for category_id, weight in categories:
            # Get assignments for this category
            self.cursor.execute('''
            SELECT earned_points, max_points 
            FROM assignments 
            WHERE category_id = ?
            ''', (category_id,))
            assignments = self.cursor.fetchall()

            if assignments:
                category_earned = sum(earned for earned, _ in assignments)
                category_max = sum(max_points for _, max_points in assignments)
                category_percentage = (category_earned / category_max) if category_max > 0 else 0
                total_weighted_grade += category_percentage * weight
                total_weight_used += weight

        final_grade = (total_weighted_grade / total_weight_used * 100) if total_weight_used > 0 else 0
        return round(final_grade, 2)

    def get_course_assignments(self, course_id: int):
        """Get all assignments for a course with their details."""
        self.cursor.execute('''
        SELECT a.title, a.max_points, a.earned_points, a.entry_date,
               c.category_name, c.weight,
               (a.earned_points / a.max_points * c.weight) as weighted_points
        FROM assignments a
        JOIN categories c ON a.category_id = c.category_id
        WHERE a.course_id = ?
        ORDER BY a.entry_date DESC
        ''', (course_id,))
        return self.cursor.fetchall()

    def get_course_categories(self, course_id: int):
        """Get all categories and their weights for a course."""
        self.cursor.execute('''
        SELECT category_name, weight
        FROM categories
        WHERE course_id = ?
        ORDER BY category_name
        ''', (course_id,))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()


def main():
    gradebook = Gradebook()

    # Add your Fall 2024 courses
    bio_seminar = gradebook.add_course("Biology Seminar (BIO 302)", "Fall 2024")
    evolution = gradebook.add_course("Evolution (BIO 515)", "Fall 2024")
    immuno_lecture = gradebook.add_course("Immunology Lecture (BIO 511)", "Fall 2024")
    immuno_lab = gradebook.add_course("Immunology Lab (BIO 511)", "Fall 2024")
    biochem = gradebook.add_course("Introduction to Biochemistry (CHM 352)", "Fall 2024")
    orgo = gradebook.add_course("Organic Chemistry II (CHM 343)", "Fall 2024")

    # Example category weights for each course
    # Note: You should adjust these weights according to your course syllabi

    # Biology Seminar categories
    bio_seminar_categories = [
        ("Participation", 0.20),
        ("Presentations", 0.40),
        ("Assignments", 0.40)
    ]
    gradebook.add_categories(bio_seminar, bio_seminar_categories)

    # Evolution categories
    evolution_categories = [
        ("Exams", 0.50),
        ("Lab Reports", 0.30),
        ("Homework", 0.20)
    ]
    gradebook.add_categories(evolution, evolution_categories)

    # Immunology Lecture categories
    immuno_lecture_categories = [
        ("Exams", 0.60),
        ("Quizzes", 0.25),
        ("Homework", 0.15)
    ]
    gradebook.add_categories(immuno_lecture, immuno_lecture_categories)

    # Immunology Lab categories
    immuno_lab_categories = [
        ("Lab Reports", 0.60),
        ("Lab Participation", 0.20),
        ("Lab Practical", 0.20)
    ]
    gradebook.add_categories(immuno_lab, immuno_lab_categories)

    # Biochemistry categories
    biochem_categories = [
        ("Exams", 0.50),
        ("Quizzes", 0.25),
        ("Homework", 0.25)
    ]
    gradebook.add_categories(biochem, biochem_categories)

    # Organic Chemistry II categories
    orgo_categories = [
        ("Exams", 0.55),
        ("Lab Reports", 0.25),
        ("Homework", 0.20)
    ]
    gradebook.add_categories(orgo, orgo_categories)

    # Print all courses and their category weights
    courses = [
        (bio_seminar, "Biology Seminar"),
        (evolution, "Evolution"),
        (immuno_lecture, "Immunology Lecture"),
        (immuno_lab, "Immunology Lab"),
        (biochem, "Biochemistry"),
        (orgo, "Organic Chemistry II")
    ]

    for course_id, course_name in courses:
        print(f"\n{course_name} Categories:")
        for name, weight in gradebook.get_course_categories(course_id):
            print(f"- {name}: {weight * 100}%")

    gradebook.close()
if __name__ == "__main__":
    main()