from database.db_manager import DatabaseManager
from datetime import datetime, date

class FinanceManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def add_transaction(self, farmer_id, transaction_type, category, amount, description=None, transaction_date=None):
        """Add a new financial transaction"""
        if not transaction_date:
            transaction_date = date.today().strftime('%Y-%m-%d')
        
        query = '''
            INSERT INTO transactions (farmer_id, type, category, amount, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        params = (farmer_id, transaction_type, category, amount, description, transaction_date)
        return self.db.execute_query(query, params)
    
    def get_transactions(self, farmer_id=None, start_date=None, end_date=None, transaction_type=None):
        """Get transactions with optional filters"""
        base_query = '''
            SELECT t.*, f.name as farmer_name
            FROM transactions t
            JOIN farmers f ON t.farmer_id = f.farmer_id
            WHERE 1=1
        '''
        params = []
        
        if farmer_id:
            base_query += " AND t.farmer_id = ?"
            params.append(farmer_id)
        
        if start_date:
            base_query += " AND t.date >= ?"
            params.append(start_date)
        
        if end_date:
            base_query += " AND t.date <= ?"
            params.append(end_date)
        
        if transaction_type:
            base_query += " AND t.type = ?"
            params.append(transaction_type)
        
        base_query += " ORDER BY t.date DESC"
        
        return self.db.execute_query(base_query, params)
    
    def get_financial_summary(self):
        """Get financial summary"""
        try:
            # Get total income
            self.db.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) as total_income 
                FROM transactions 
                WHERE type = 'income'
            """)
            total_income = self.db.cursor.fetchone()[0]
            
            # Get total expenses
            self.db.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) as total_expenses 
                FROM transactions 
                WHERE type = 'expense'
            """)
            total_expenses = self.db.cursor.fetchone()[0]
            
            # Calculate net profit
            net_profit = total_income - total_expenses
            
            return {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_profit': net_profit
            }
        except Exception as e:
            print(f"Error getting financial summary: {e}")
            return {'total_income': 0, 'total_expenses': 0, 'net_profit': 0}
    
    def get_category_breakdown(self):
        """Get breakdown by category"""
        try:
            self.db.cursor.execute("""
                SELECT category, SUM(amount) as total
                FROM transactions
                GROUP BY category
                ORDER BY total DESC
            """)
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error getting category breakdown: {e}")
            return []
    
    def get_monthly_summary(self):
        """Get monthly financial summary"""
        try:
            self.db.cursor.execute("""
                SELECT 
                    strftime('%m', date) as month,
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as monthly_income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as monthly_expenses,
                    SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) as monthly_profit
                FROM transactions
                GROUP BY strftime('%m', date)
                ORDER BY month
            """)
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error getting monthly summary: {e}")
            return []
    
    def get_top_expenses(self, limit=5):
        """Get top expenses"""
        try:
            self.db.cursor.execute("""
                SELECT description, amount, date
                FROM transactions
                WHERE type = 'expense'
                ORDER BY amount DESC
                LIMIT ?
            """, (limit,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error getting top expenses: {e}")
            return []
    
    def get_top_income(self, limit=5):
        """Get top income sources"""
        try:
            self.db.cursor.execute("""
                SELECT description, amount, date
                FROM transactions
                WHERE type = 'income'
                ORDER BY amount DESC
                LIMIT ?
            """, (limit,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error getting top income: {e}")
            return []
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction"""
        query = "DELETE FROM transactions WHERE transaction_id = ?"
        return self.db.execute_query(query, (transaction_id,))
    
    def update_transaction(self, transaction_id, transaction_type=None, category=None, amount=None, description=None):
        """Update a transaction"""
        # Get current transaction data
        query = "SELECT * FROM transactions WHERE transaction_id = ?"
        current = self.db.execute_query(query, (transaction_id,))
        if not current:
            return False
        
        current = current[0]
        
        # Update only provided fields
        transaction_type = transaction_type if transaction_type is not None else current['type']
        category = category if category is not None else current['category']
        amount = amount if amount is not None else current['amount']
        description = description if description is not None else current['description']
        
        update_query = '''
            UPDATE transactions 
            SET type = ?, category = ?, amount = ?, description = ?
            WHERE transaction_id = ?
        '''
        params = (transaction_type, category, amount, description, transaction_id)
        return self.db.execute_query(update_query, params) 