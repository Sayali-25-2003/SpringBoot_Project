import pymysql
import csv

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="pass@word1",
    database="attendance_db"
)
cursor = conn.cursor()

# Create the attendance table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(50),
    name VARCHAR(255),
    course VARCHAR(100),
    date DATE,
    status VARCHAR(10)
)
""")
conn.commit()

# Function to insert a new record
def insert_record():
    roll_number = input("Enter Roll No.: ")
    name = input("Enter Name: ")
    course = input("Enter Course: ")
    date = input("Enter Date (YYYY-MM-DD): ")
    status = input("Enter Status (Present/Absent): ")
    cursor.execute("""
        INSERT INTO attendance (roll_number, name, course, date, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (roll_number, name, course, date, status))
    conn.commit()
    print("✅ Record inserted successfully.")

# Function to view all records
def view_records():
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    print("\n--- Attendance Records ---")
    for row in records:
        print(f" Roll No.: {row[1]}, Name: {row[2]}, Course: {row[3]}, Date: {row[4]}, Status: {row[5]}")

# Function to update a record's status
def update_record():
    record_id = input("Enter ID to update: ")
    status = input("Enter new Status (Present/Absent): ")
    cursor.execute("UPDATE attendance SET status = %s WHERE id = %s", (status, record_id))
    conn.commit()
    print("✅ Record updated successfully.")

# Function to delete a record
def delete_record():
    record_id = input("Enter ID to delete: ")
    cursor.execute("DELETE FROM attendance WHERE id = %s", (record_id,))
    conn.commit()
    print("✅ Record deleted successfully.")

# Function to export records to CSV
def export_to_csv():
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    with open("attendance_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Roll No.", "Name", "Course", "Date", "Status"])
        writer.writerows(rows)
    print("📁 Data exported to attendance_export.csv")

# Main menu loop
def menu():
    while True:
        print("\n--- Attendance Management System ---")
        print("1. Insert Record")
        print("2. View Records")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. Export to CSV")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            insert_record()
        elif choice == "2":
            view_records()
        elif choice == "3":
            update_record()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            export_to_csv()
        elif choice == "6":
            print("👋 Exiting Attendance Management System.")
            break
        else:
            print("❌ Invalid choice. Try again.")

# Run the menu
menu()

# Close the database connection
cursor.close()
conn.close()

