import sqlite3

def delete_all_records(db_name):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        
        # Delete all records from each table
        cursor.execute("DELETE FROM OrderItems;")
        cursor.execute("DELETE FROM Orders;")
        cursor.execute("DELETE FROM MenuItems;")
        cursor.execute("DELETE FROM Customers;")
        
        # Optional: Reset the auto-increment counter
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='OrderItems';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Orders';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='MenuItems';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Customers';")
        
        # Commit the changes and close the connection
        connection.commit()
        print("All records have been deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close()

# Usage
if __name__ == "__main__":
    delete_all_records("restaurant.db")