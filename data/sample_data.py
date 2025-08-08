from database.db_manager import DatabaseManager
import random

def load_sample_data():
    """Load sample data into the database"""
    try:
        from modules.farmer import FarmerManager
        from modules.crop import CropManager
        from modules.finance import FinanceManager
        
        farmer_manager = FarmerManager()
        crop_manager = CropManager()
        finance_manager = FinanceManager()
        
        # Add sample farmers
        farmers_data = [
            ("John Smith", "555-0101", "john@farm.com", 150.5),
            ("Mary Johnson", "555-0102", "mary@farm.com", 200.0),
            ("David Wilson", "555-0103", "david@farm.com", 75.25),
            ("Sarah Brown", "555-0104", "sarah@farm.com", 120.75),
            ("Michael Davis", "555-0105", "michael@farm.com", 300.0)
        ]
        
        for name, phone, email, farm_size in farmers_data:
            farmer_manager.add_farmer(name, phone, email, farm_size)
        
        # Add sample crops
        crops_data = [
            ("Wheat", "Winter Wheat", 120, 50.0, 2500.00),
            ("Corn", "Sweet Corn", 90, 180.0, 1800.00),
            ("Soybeans", "Roundup Ready", 100, 45.0, 3200.00),
            ("Rice", "Basmati", 150, 60.0, 4000.00),
            ("Cotton", "Bollgard", 180, 800.0, 150.00)
        ]
        
        for name, variety, growth_period, yield_per_acre, price in crops_data:
            crop_manager.add_crop(name, variety, growth_period, yield_per_acre, price)
        
        # Add sample plantings
        plantings_data = [
            (1, 1, "2024-03-15", 25.0, "2024-07-15", "Growing"),
            (2, 2, "2024-04-01", 30.0, "2024-07-01", "Growing"),
            (3, 3, "2024-03-20", 20.0, "2024-06-20", "Growing"),
            (4, 4, "2024-05-01", 15.0, "2024-09-01", "Planned"),
            (5, 5, "2024-04-15", 40.0, "2024-10-15", "Growing")
        ]
        
        for farmer_id, crop_id, planting_date, area, harvest_date, status in plantings_data:
            crop_manager.add_planting(farmer_id, crop_id, planting_date, area, harvest_date, status)
        
        # Add sample financial transactions
        transactions_data = [
            (1, "income", "Crop Sale", 125000.00, "2024-06-15", "Wheat harvest sale"),
            (2, "income", "Crop Sale", 108000.00, "2024-07-01", "Corn harvest sale"),
            (3, "income", "Crop Sale", 64000.00, "2024-06-20", "Soybean harvest sale"),
            (1, "expense", "Fertilizer", 15000.00, "2024-03-10", "Spring fertilizer application"),
            (2, "expense", "Seeds", 12000.00, "2024-04-01", "Corn seeds purchase"),
            (3, "expense", "Pesticides", 8000.00, "2024-05-15", "Pest control chemicals"),
            (4, "expense", "Equipment", 25000.00, "2024-02-20", "Tractor maintenance"),
            (5, "income", "Crop Sale", 60000.00, "2024-08-15", "Rice harvest sale"),
            (1, "expense", "Labor", 20000.00, "2024-06-01", "Harvesting labor costs"),
            (2, "expense", "Irrigation", 5000.00, "2024-05-01", "Water system maintenance")
        ]
        
        for farmer_id, trans_type, category, amount, date, description in transactions_data:
            finance_manager.add_transaction(farmer_id, trans_type, category, amount, date, description)
        
        print("✅ Sample data loaded successfully!")
        print(f"📊 Added {len(farmers_data)} farmers")
        print(f"🌱 Added {len(crops_data)} crops")
        print(f"🌾 Added {len(plantings_data)} plantings")
        print(f"💰 Added {len(transactions_data)} financial transactions")
        
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")

if __name__ == "__main__":
    load_sample_data() 