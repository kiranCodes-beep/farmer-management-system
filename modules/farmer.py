from database.db_manager import DatabaseManager
from datetime import datetime

class FarmerManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def add_farmer(self, name, phone=None, email=None, address=None, farm_size=None):
        """Add a new farmer to the database"""
        query = '''
            INSERT INTO farmers (name, phone, email, address, farm_size)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (name, phone, email, address, farm_size)
        return self.db.execute_query(query, params)
    
    def get_all_farmers(self):
        """Get all farmers from the database"""
        query = "SELECT * FROM farmers ORDER BY name"
        return self.db.execute_query(query)
    
    def get_farmer_by_id(self, farmer_id):
        """Get a specific farmer by ID"""
        query = "SELECT * FROM farmers WHERE farmer_id = ?"
        result = self.db.execute_query(query, (farmer_id,))
        return result[0] if result else None
    
    def update_farmer(self, farmer_id, name=None, phone=None, email=None, address=None, farm_size=None):
        """Update farmer information"""
        # Get current farmer data
        current = self.get_farmer_by_id(farmer_id)
        if not current:
            return False
        
        # Update only provided fields
        name = name if name is not None else current['name']
        phone = phone if phone is not None else current['phone']
        email = email if email is not None else current['email']
        address = address if address is not None else current['address']
        farm_size = farm_size if farm_size is not None else current['farm_size']
        
        query = '''
            UPDATE farmers 
            SET name = ?, phone = ?, email = ?, address = ?, farm_size = ?
            WHERE farmer_id = ?
        '''
        params = (name, phone, email, address, farm_size, farmer_id)
        return self.db.execute_query(query, params)
    
    def delete_farmer(self, farmer_id):
        """Delete a farmer from the database"""
        query = "DELETE FROM farmers WHERE farmer_id = ?"
        return self.db.execute_query(query, (farmer_id,))
    
    def search_farmers(self, search_term):
        """Search farmers by name, phone, or email"""
        query = '''
            SELECT * FROM farmers 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY name
        '''
        search_pattern = f"%{search_term}%"
        params = (search_pattern, search_pattern, search_pattern)
        return self.db.execute_query(query, params)
    
    def get_farmer_statistics(self, farmer_id):
        """Get statistics for a specific farmer"""
        # Get planting information
        planting_query = '''
            SELECT COUNT(*) as total_plantings,
                   SUM(area_planted) as total_area
            FROM plantings 
            WHERE farmer_id = ?
        '''
        planting_stats = self.db.execute_query(planting_query, (farmer_id,))
        
        # Get financial information
        finance_query = '''
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expenses
            FROM transactions 
            WHERE farmer_id = ?
        '''
        finance_stats = self.db.execute_query(finance_query, (farmer_id,))
        
        return {
            'planting_stats': planting_stats[0] if planting_stats else {},
            'finance_stats': finance_stats[0] if finance_stats else {}
        } 