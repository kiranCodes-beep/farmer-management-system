import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from modules.farmer import FarmerManager
from modules.crop import CropManager
from modules.finance import FinanceManager
from gui.main_window import MainWindow

class FarmerManagementSystem:
    def __init__(self, root, user=None):
        self.root = root
        self.user = user  # Store user information
        
        self.root.title("Farmer Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize managers
        self.db_manager = DatabaseManager()
        self.farmer_manager = FarmerManager()
        self.crop_manager = CropManager()
        self.finance_manager = FinanceManager()
        
        # Create main window
        self.main_window = MainWindow(
            self.root, 
            self.farmer_manager, 
            self.crop_manager, 
            self.finance_manager,
            self.user
        )
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {str(e)}")
        finally:
            # Cleanup
            if hasattr(self, 'db_manager'):
                self.db_manager.disconnect()

def main():
    """Main entry point"""
    try:
        # Check if user is provided (from login)
        if len(sys.argv) > 1 and sys.argv[1] == '--no-login':
            # Direct access without login
            root = tk.Tk()
            app = FarmerManagementSystem(root)
            app.run()
        else:
            # Start with login
            from gui.login_window import LoginWindow
            root = tk.Tk()
            login_app = LoginWindow(root)
            login_app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 