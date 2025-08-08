from database.db_manager import DatabaseManager
from datetime import datetime, timedelta

class CropManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def add_crop(self, name, variety=None, growth_period=None, yield_per_acre=None, price_per_unit=None):
        """Add a new crop type to the database"""
        query = '''
            INSERT INTO crops (name, variety, growth_period, yield_per_acre, price_per_unit)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (name, variety, growth_period, yield_per_acre, price_per_unit)
        return self.db.execute_query(query, params)
    
    def get_all_crops(self):
        """Get all crops from the database"""
        query = "SELECT * FROM crops ORDER BY name"
        return self.db.execute_query(query)
    
    def get_crop_by_id(self, crop_id):
        """Get a specific crop by ID"""
        query = "SELECT * FROM crops WHERE crop_id = ?"
        result = self.db.execute_query(query, (crop_id,))
        return result[0] if result else None
    
    def add_planting(self, farmer_id, crop_id, planting_date, area_planted, expected_harvest_date=None):
        """Add a new planting record"""
        if not expected_harvest_date:
            # Calculate expected harvest date based on crop growth period
            crop = self.get_crop_by_id(crop_id)
            if crop and crop['growth_period']:
                planting_dt = datetime.strptime(planting_date, '%Y-%m-%d')
                expected_harvest_date = (planting_dt + timedelta(days=crop['growth_period'])).strftime('%Y-%m-%d')
        
        query = '''
            INSERT INTO plantings (farmer_id, crop_id, planting_date, area_planted, expected_harvest_date)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (farmer_id, crop_id, planting_date, area_planted, expected_harvest_date)
        return self.db.execute_query(query, params)
    
    def get_all_plantings(self, farmer_id=None):
        """Get all planting records, optionally filtered by farmer"""
        if farmer_id:
            query = '''
                SELECT p.*, f.name as farmer_name, c.name as crop_name
                FROM plantings p
                JOIN farmers f ON p.farmer_id = f.farmer_id
                JOIN crops c ON p.crop_id = c.crop_id
                WHERE p.farmer_id = ?
                ORDER BY p.planting_date DESC
            '''
            return self.db.execute_query(query, (farmer_id,))
        else:
            query = '''
                SELECT p.*, f.name as farmer_name, c.name as crop_name
                FROM plantings p
                JOIN farmers f ON p.farmer_id = f.farmer_id
                JOIN crops c ON p.crop_id = c.crop_id
                ORDER BY p.planting_date DESC
            '''
            return self.db.execute_query(query)
    
    def update_planting_status(self, planting_id, status):
        """Update the status of a planting (Growing, Harvested, Failed)"""
        query = "UPDATE plantings SET status = ? WHERE planting_id = ?"
        return self.db.execute_query(query, (status, planting_id))
    
    def get_planting_by_id(self, planting_id):
        """Get a specific planting record"""
        query = '''
            SELECT p.*, f.name as farmer_name, c.name as crop_name
            FROM plantings p
            JOIN farmers f ON p.farmer_id = f.farmer_id
            JOIN crops c ON p.crop_id = c.crop_id
            WHERE p.planting_id = ?
        '''
        result = self.db.execute_query(query, (planting_id,))
        return result[0] if result else None
    
    def get_crop_statistics(self):
        """Get statistics about crops and plantings"""
        # Total plantings by crop
        crop_stats_query = '''
            SELECT 
                c.name as crop_name,
                COUNT(p.planting_id) as total_plantings,
                SUM(p.area_planted) as total_area,
                AVG(p.area_planted) as avg_area
            FROM crops c
            LEFT JOIN plantings p ON c.crop_id = p.crop_id
            GROUP BY c.crop_id, c.name
            ORDER BY total_plantings DESC
        '''
        
        # Current growing crops
        growing_crops_query = '''
            SELECT 
                c.name as crop_name,
                COUNT(*) as growing_count,
                SUM(p.area_planted) as total_growing_area
            FROM plantings p
            JOIN crops c ON p.crop_id = c.crop_id
            WHERE p.status = 'Growing'
            GROUP BY c.crop_id, c.name
        '''
        
        return {
            'crop_stats': self.db.execute_query(crop_stats_query),
            'growing_crops': self.db.execute_query(growing_crops_query)
        }
    
    def get_harvest_schedule(self, days_ahead=30):
        """Get upcoming harvests in the next N days"""
        query = '''
            SELECT 
                p.planting_id,
                f.name as farmer_name,
                c.name as crop_name,
                p.planting_date,
                p.expected_harvest_date,
                p.area_planted,
                p.status
            FROM plantings p
            JOIN farmers f ON p.farmer_id = f.farmer_id
            JOIN crops c ON p.crop_id = c.crop_id
            WHERE p.status = 'Growing'
            AND p.expected_harvest_date <= date('now', '+' || ? || ' days')
            ORDER BY p.expected_harvest_date
        '''
        return self.db.execute_query(query, (days_ahead,)) 