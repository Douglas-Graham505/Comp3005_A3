
# IMPORTS
# 'closing' Guarantes that an objects .close() method is called automatically
# when the 'with' block finishes, preventing leaked database connections
from contextlib import closing

# 'Psycopg2' is the PostgreSQL database adapter for Python.
import psycopg2

# 'Error' is the base exception class for database errors in psycopg2.
# 'IntegrityError' catches constraint violations (like duplicate UNIQUE emails).
from psycopg2 import Error, IntegrityError



# DATABASE CONFIGURATION

DB_CONFIG = {
    "host": "localhost",       
    "port": "5432",            
    "database": "Comp3005A3",  
    "user": "postgres",        
    "password": "password",   
}



# HELPER FUNCTION: DATABASE CONNECTION

def get_connection():
    """Establishes and returns a live network connection to PostgreSQL."""
    # '**DB_CONFIG' unpacks the dictionary into keyword arguments.
    return psycopg2.connect(**DB_CONFIG)



# CRUD OPERATION : READ (SELECT)

def getAllStudents():
    """Retrieves and displays all records from the students table."""
    # Sort by student_id ascending so records always display in order.
    query = "SELECT * FROM students ORDER BY student_id ASC;"

    try:
        with closing(get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                records = cursor.fetchall()

                print("\n--- Current Students ---")
                if not records:
                    print("No student records found.")
                else:
                    # Each  row is a tuple: (student_id, first_name, last_name, email, enrollment_date)
                    for row in records:
                        print(
                            f"ID: {row[0]} | Name: {row[1]} {row[2]} | "
                            f"Email: {row[3]} | Enrolled: {row[4]}"
                        )
                print("------------------------\n")

    except Error as e:
        print(f"Error retrieving students: {e}")



# CRUD OPERATION : CREATE (INSERT)

def addStudent(first_name, last_name, email, enrollment_date):
    """Inserts a new student record into the students table."""
    # Parameterized '%s' placeholders protect against SQL injection.
    # 'RETURNING student_id' returns the auto-generated SERIAL primary key.
    query = """
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id;
    """
    try:
        with closing(get_connection()) as conn:
            # 'with conn:' automatically commits on success or rolls back on error.
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        query, (first_name, last_name, email, enrollment_date)
                    )
                    # Extract the integer ID from the returned single element tuple)
                    new_id = cursor.fetchone()[0]
                    print(
                        f"Added student '{first_name} {last_name}' with ID: {new_id}"
                    )

    except IntegrityError:
        print(
            f"Error: The email '{email}' already exists or required fields are missing."
        )
    except Error as e:
        print(f"Error adding student: {e}")



# CRUD OPERATION : UPDATE

def updateStudentEmail(student_id, new_email):
    """Updates the email address for a student with the specified student_id."""
    query = "UPDATE students SET email = %s WHERE student_id = %s;"

    try:
        with closing(get_connection()) as conn:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (new_email, student_id))

                    # 'Rowcount' checks how many rows were actually updated.
                    if cursor.rowcount > 0:
                        print(
                            f"Updated email for student ID {student_id} to '{new_email}'."
                        )
                    else:
                        print(f"No student found with ID {student_id}.")

    except IntegrityError:
        print(f"Error: The email '{new_email}' is already in use.")
    except Error as e:
        print(f"Error updating student email: {e}")



# CRUD OPERATION : DELETE

def deleteStudent(student_id):
    """Deletes the record of the student with the specified student_id."""
    query = "DELETE FROM students WHERE student_id = %s;"

    try:
        with closing(get_connection()) as conn:
            with conn:
                with conn.cursor() as cursor:
                    # Trailing comma makes (student_id,) a 1-element tuple.
                    cursor.execute(query, (student_id,))

                    if cursor.rowcount > 0:
                        print(f"Deleted student with ID {student_id}.")
                    else:
                        print(f"No student found with ID {student_id}.")

    except Error as e:
        print(f"Error deleting student: {e}")



# AUTOMATED DEMONSTRATION FUNCTION

def runDemo():
    """Runs a pre-scripted sequence demonstrating all four CRUD operations."""
    print("\n=== Starting Automated CRUD Demo ===")

    print("1. Initial records:")
    getAllStudents()

    print("2. Adding a new student:")
    addStudent("Alice", "Wonder", "alice.wonder@example.com", "2023-09-05")
    getAllStudents()

    print("3. Updating a student's email:")
    updateStudentEmail(1, "john.newemail@example.com")
    getAllStudents()

    print("4. Deleting a student:")
    deleteStudent(2)
    getAllStudents()

    print("=== Demo Complete ===\n")



# MAIN PROGRAM ENTRY POINT & INTERACTIVE MENU

if __name__ == "__main__":
    while True:
        print("=== Student Management System ===")
        print("1. View all students")
        print("2. add a student")
        print("3. Update student email")
        print("4. Delete a student")
        print("5. run automated CRUD demo")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            getAllStudents()

        elif choice == "2":
            fname = input("First name: ").strip()
            lname = input("Last name: ").strip()
            email = input("Email : ").strip()
            date = input("Enrollment date (YYYY-MM-DD): ").strip()
            addStudent(fname, lname, email, date)

        elif choice == "3":
            try:
                sid = int(input("Student ID to update: "))
                new_email = input("New email: ").strip()
                updateStudentEmail(sid, new_email)
            except ValueError:
                print("Invalid input. Student ID must be a number.")

        elif choice == "4":
            try:
                sid = int(input("Student ID to delete: "))
                deleteStudent(sid)
            except ValueError:
                print("Invalid input. Student ID must be a number.")

        elif choice == "5":
            runDemo()

        elif choice == "6":
            print("Exiting program.")
            break

        else:
            print(" Please enter a number between 1 and 6.\n")
