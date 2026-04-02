import sqlite3

def alter_database():
    try:
        # 1. Database connection
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # 2. 'reservations' table-la 'mode' column add panrom
        # 'IF NOT EXISTS' SQLite-la direct-ah alter-ku varathu, 
        # so try-except block use panrom.
        print("Updating database structure...")
        
        cursor.execute("ALTER TABLE reservations ADD COLUMN mode TEXT")
        
        conn.commit()
        print("Column 'mode' added successfully to 'reservations' table! ✅")

    except sqlite3.OperationalError as e:
        # Oru velai column munnadiye irundha intha error varum
        if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
            print("Column 'mode' already exists. No changes needed. 👍")
        else:
            print(f"Operational Error: {e} ❌")
            
    except Exception as e:
        print(f"An error occurred: {e} ❌")
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    alter_database()