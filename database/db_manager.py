import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="farm_management.db"):
        self.db_path = db_path
        self.connection = None
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def create_tables(self):
        """Create all necessary tables"""
        self.connect()
        
        # Farmers table
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                farm_size REAL,
                registration_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Crops table
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS crops (
                crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                variety TEXT,
                growth_period INTEGER,
                yield_per_acre REAL,
                price_per_unit REAL
            )
        ''')
        
        # Plantings table
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS plantings (
                planting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER,
                crop_id INTEGER,
                planting_date DATE,
                area_planted REAL,
                expected_harvest_date DATE,
                status TEXT DEFAULT 'Growing',
                FOREIGN KEY (farmer_id) REFERENCES farmers (farmer_id),
                FOREIGN KEY (crop_id) REFERENCES crops (crop_id)
            )
        ''')
        
        # Equipment table
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS equipment (
                equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT,
                purchase_date DATE,
                cost REAL,
                status TEXT DEFAULT 'Active'
            )
        ''')
        
        # Inventory table
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER,
                unit TEXT,
                cost_per_unit REAL,
                supplier TEXT
            )
        ''')
        
        # Transactions table
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER,
                type TEXT, -- 'income' or 'expense'
                category TEXT,
                amount REAL,
                description TEXT,
                date DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (farmer_id) REFERENCES farmers (farmer_id)
            )
        ''')
        
        # Weather data table
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                temperature REAL,
                humidity REAL,
                rainfall REAL,
                description TEXT
            )
        ''')
        
        self.connection.commit()
        self.disconnect()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            self.connect()
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Query execution error: {e}")
            return None
        finally:
            self.disconnect()
    
    def backup_database(self, backup_path):
        """Create a backup of the database"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"Backup error: {e}")
            return False 