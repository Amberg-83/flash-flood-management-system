import sqlite3


def create_database():

    conn = sqlite3.connect("flood_system.db")
    cur = conn.cursor()

    # ================= USERS TABLE =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # ================= FLOOD SIMULATION DATA =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS flood_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT,
        rainfall REAL,
        river_level REAL,
        population_density INTEGER,
        drainage_capacity INTEGER,
        resources_deployed INTEGER,
        affected_population INTEGER,
        date TEXT
    )
    """)

    # ================= CIVILIAN REPORTS =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS civilian_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        description TEXT,
        severity TEXT,
        status TEXT,
        date TEXT
    )
    """)

    # ================= AI PREDICTIONS (NEW) =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ai_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT,
        rainfall REAL,
        river_level REAL,
        pop_density INTEGER,
        drainage INTEGER,
        resources INTEGER,
        predicted_affected INTEGER,
        confidence REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully")


# Run directly
if __name__ == "__main__":
    create_database()