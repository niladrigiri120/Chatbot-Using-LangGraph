import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# Create Connection to Database
conn = sqlite3.connect(database= "chatterly.db", check_same_thread= False)

# Create table
def create_table():
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS id_title
                   (thread_id TEXT PRIMARY KEY,
                    title TEXT,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)
    
    conn.commit()

# Save table
def save_table(thread_id, title):
    cursor = conn.cursor()

    cursor.execute(
        """INSERT OR REPLACE INTO id_title 
            (thread_id, title) VALUES (?, ?)""",(thread_id, title),
                )
    
    conn.commit()

# Load table
def load_table():
    cursor = conn.cursor()

    cursor.execute(
        """SELECT thread_id, title FROM id_title
        ORDER BY time DESC
        """)
    
    rows = cursor.fetchall()

    return [{"id": row[0], "title": row[1]} for row in rows]

# Update table based on recent time
def update_table(thread_id):
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE id_title
        SET time = CURRENT_TIMESTAMP
        WHERE thread_id = ?
    """, (thread_id,))

    conn.commit()

# Checkpoint
checkpointer = SqliteSaver(conn = conn)