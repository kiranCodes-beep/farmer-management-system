#!/usr/bin/env python3
"""
Test script for Farmer Management System
This script tests the basic functionality of the system
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from modules.farmer import FarmerManager
from modules.crop import CropManager
from modules.finance import FinanceManager
from data.sample_data import load_sample_data

def test_database_connection():
    """Test database connection and table creation"""
    print("Testing database connection...")
    try:
        db = DatabaseManager()
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_farmer_operations():
    """Test farmer management operations"""
    print("\nTesting farmer operations...")
    try:
        farmer_mgr = FarmerManager()
        
        # Test adding a farmer
        farmer_id = farmer_mgr.add_farmer("Test Farmer", "555-1234", "test@email.com", "Test Address", 100.0)
        if farmer_id:
            print("✓ Add farmer successful")
        else:
            print("✗ Add farmer failed")
            return False
        
        # Test getting all farmers
        farmers = farmer_mgr.get_all_farmers()
        if farmers:
            print(f"✓ Get farmers successful - Found {len(farmers)} farmers")
        else:
            print("✗ Get farmers failed")
            return False
        
        # Test searching farmers
        search_results = farmer_mgr.search_farmers("Test")
        if search_results:
            print("✓ Search farmers successful")
        else:
            print("✗ Search farmers failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Farmer operations failed: {e}")
        return False

def test_crop_operations():
    """Test crop management operations"""
    print("\nTesting crop operations...")
    try:
        crop_mgr = CropManager()
        
        # Test adding a crop
        crop_id = crop_mgr.add_crop("Test Crop", "Test Variety", 90, 100.0, 5.0)
        if crop_id:
            print("✓ Add crop successful")
        else:
            print("✗ Add crop failed")
            return False
        
        # Test getting all crops
        crops = crop_mgr.get_all_crops()
        if crops:
            print(f"✓ Get crops successful - Found {len(crops)} crops")
        else:
            print("✗ Get crops failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Crop operations failed: {e}")
        return False

def test_finance_operations():
    """Test finance management operations"""
    print("\nTesting finance operations...")
    try:
        finance_mgr = FinanceManager()
        
        # Get a farmer for testing
        farmer_mgr = FarmerManager()
        farmers = farmer_mgr.get_all_farmers()
        if not farmers:
            print("✗ No farmers available for finance testing")
            return False
        
        farmer_id = farmers[0]['farmer_id']
        
        # Test adding a transaction
        transaction_id = finance_mgr.add_transaction(farmer_id, "income", "Test Income", 1000.0, "Test transaction")
        if transaction_id:
            print("✓ Add transaction successful")
        else:
            print("✗ Add transaction failed")
            return False
        
        # Test getting transactions
        transactions = finance_mgr.get_transactions()
        if transactions:
            print(f"✓ Get transactions successful - Found {len(transactions)} transactions")
        else:
            print("✗ Get transactions failed")
            return False
        
        # Test financial summary
        summary = finance_mgr.get_financial_summary()
        if summary:
            print("✓ Financial summary successful")
        else:
            print("✗ Financial summary failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Finance operations failed: {e}")
        return False

def test_sample_data():
    """Test loading sample data"""
    print("\nTesting sample data loading...")
    try:
        load_sample_data()
        print("✓ Sample data loading successful")
        return True
    except Exception as e:
        print(f"✗ Sample data loading failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("Farmer Management System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Farmer Operations", test_farmer_operations),
        ("Crop Operations", test_crop_operations),
        ("Finance Operations", test_finance_operations),
        ("Sample Data Loading", test_sample_data),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! System is ready to use.")
        print("\nTo run the application:")
        print("python main.py")
        print("\nTo load sample data:")
        print("python data/sample_data.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 