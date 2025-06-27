import sqlite3
import datetime

class Journal:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_entries_table()
        self.create_salvage_wrecks_table()
        self.create_mining_locations_table()

    def __del__(self):
        self.conn.close()

    def create_entries_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    system TEXT NOT NULL,
                    planet TEXT,
                    notes TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

    def add_entry(self, title, system, planet, notes):
        timestamp = datetime.datetime.now().isoformat()
        with self.conn:
            self.conn.execute(
                "INSERT INTO entries (title, system, planet, notes, timestamp) VALUES (?, ?, ?, ?, ?)",
                (title, system, planet, notes, timestamp)
            )

    def get_all_entries(self):
        with self.conn:
            return self.conn.execute("SELECT id, title, system, planet, notes, timestamp FROM entries").fetchall()

    def update_entry(self, entry_id, title, system, planet, notes):
        with self.conn:
            self.conn.execute(
                "UPDATE entries SET title = ?, system = ?, planet = ?, notes = ? WHERE id = ?",
                (title, system, planet, notes, entry_id)
            )

    def delete_entry(self, entry_id):
        with self.conn:
            self.conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))

    def create_salvage_wrecks_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS salvage_wrecks (
                    id INTEGER PRIMARY KEY,
                    system TEXT NOT NULL,
                    location_description TEXT NOT NULL,
                    ship_type TEXT,
                    notes TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

    def add_salvage_wreck(self, system, location_description, ship_type, notes):
        timestamp = datetime.datetime.now().isoformat()
        with self.conn:
            self.conn.execute(
                "INSERT INTO salvage_wrecks (system, location_description, ship_type, notes, timestamp) VALUES (?, ?, ?, ?, ?)",
                (system, location_description, ship_type, notes, timestamp)
            )

    def get_all_salvage_wrecks(self):
        with self.conn:
            return self.conn.execute("SELECT id, system, location_description, ship_type, notes, timestamp FROM salvage_wrecks").fetchall()

    def update_salvage_wreck(self, wreck_id, system, location_description, ship_type, notes):
        with self.conn:
            self.conn.execute(
                "UPDATE salvage_wrecks SET system = ?, location_description = ?, ship_type = ?, notes = ? WHERE id = ?",
                (system, location_description, ship_type, notes, wreck_id)
            )

    def delete_salvage_wreck(self, wreck_id):
        with self.conn:
            self.conn.execute("DELETE FROM salvage_wrecks WHERE id = ?", (wreck_id,))

    def create_mining_locations_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS mining_locations (
                    id INTEGER PRIMARY KEY,
                    system TEXT NOT NULL,
                    location_description TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    notes TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

    def add_mining_location(self, system, location_description, resource_type, notes):
        timestamp = datetime.datetime.now().isoformat()
        with self.conn:
            self.conn.execute(
                "INSERT INTO mining_locations (system, location_description, resource_type, notes, timestamp) VALUES (?, ?, ?, ?, ?)",
                (system, location_description, resource_type, notes, timestamp)
            )

    def get_all_mining_locations(self):
        with self.conn:
            return self.conn.execute("SELECT id, system, location_description, resource_type, notes, timestamp FROM mining_locations").fetchall()

    def update_mining_location(self, location_id, system, location_description, resource_type, notes):
        with self.conn:
            self.conn.execute(
                "UPDATE mining_locations SET system = ?, location_description = ?, resource_type = ?, notes = ? WHERE id = ?",
                (system, location_description, resource_type, notes, location_id)
            )

    def delete_mining_location(self, location_id):
        with self.conn:
            self.conn.execute("DELETE FROM mining_locations WHERE id = ?", (location_id,))
