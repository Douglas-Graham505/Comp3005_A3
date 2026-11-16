# COMP 3005 - Assignment 3: PostgreSQL Student CRUD Application

A Python application that connects to a PostgreSQL database to perform Create, Read, Update, and Delete (CRUD) operations on a `students` table.

## Demo Video
* **Video Demonstration:** [Insert your YouTube or Google Drive video link here]

## Prerequisites
* Python 3.x
* PostgreSQL installed and running locally
* `psycopg2-binary` library

## Setup & Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create the PostgreSQL database:**
   Open pgAdmin or `psql` and run:
   ```sql
   CREATE DATABASE "Comp3005A3";
   ```

3. **Create and populate the table:**
   Connect to the `Comp3005A3` database and run the provided `schema.sql` file:
   ```bash
   psql -U postgres -d Comp3005A3 -f schema.sql
   ```
   *(Or open `schema.sql` inside pgAdmin's Query Tool and click Execute.)*

4. **Configure database credentials:**
   Open `Comp3005A3.py` and update the `DB_CONFIG` dictionary at the top of the file with your local PostgreSQL username and password.

## Running the Application

Run the script from your terminal:
```bash
python Comp3005A3.py
```

### Menu Options
* **1:** View all students (`getAllStudents`)
* **2:** Add a new student (`addStudent`)
* **3:** Update a student's email (`updateStudentEmail`)
* **4:** Delete a student (`deleteStudent`)
* **5:** Run the automated CRUD demonstration
* **6:** Exit
