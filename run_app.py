#!/usr/bin/env python3
"""
Launcher for Farmer Management System
This script starts the application with the login system
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point"""
    try:
        # Start with login system
        from gui.login_window import LoginWindow
        import tkinter as tk
        
        root = tk.Tk()
        login_app = LoginWindow(root)
        login_app.run()
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 