import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import hashlib
import re

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Farmer Management System - Login")
        self.root.geometry("500x700")  # Made window larger
        self.root.resizable(False, False)
        self.root.configure(bg='#1e3a8a')
        
        # Center the window
        self.center_window()
        
        # Initialize database
        self.init_database()
        
        # Create UI
        self.create_widgets()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def init_database(self):
        """Initialize user database"""
        try:
            self.conn = sqlite3.connect('farm_management.db')
            self.cursor = self.conn.cursor()
            
            # Create users table if not exists
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    role TEXT DEFAULT 'user',
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create default admin user if not exists
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            if self.cursor.fetchone()[0] == 0:
                admin_password = self.hash_password("admin123")
                self.cursor.execute('''
                    INSERT INTO users (username, email, password_hash, full_name, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', 'admin@farm.com', admin_password, 'System Administrator', 'admin'))
            
            self.conn.commit()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {str(e)}")
    
    def create_widgets(self):
        """Create the login/signup interface with CSS-like styling"""
        # Main container with gradient-like background
        main_frame = tk.Frame(self.root, bg='#1e3a8a')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Inner container for content with shadow effect
        content_frame = tk.Frame(main_frame, bg='#ffffff', relief='flat', bd=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title with better styling
        title_frame = tk.Frame(content_frame, bg='#ffffff')
        title_frame.pack(pady=(40, 30))
        
        # Large emoji with better styling
        title_label = tk.Label(title_frame, text="🌾", font=("Arial", 64), 
                              bg='#ffffff', fg='#059669')
        title_label.pack()
        
        # Main title with gradient-like effect
        title_text = tk.Label(title_frame, text="Farmer Management System", 
                             font=("Arial", 28, "bold"), bg='#ffffff', fg='#1f2937')
        title_text.pack(pady=(15, 8))
        
        subtitle_label = tk.Label(title_frame, text="Secure Agricultural Management", 
                                 font=("Arial", 14), bg='#ffffff', fg='#6b7280')
        subtitle_label.pack()
        
        # Create notebook for login/signup tabs with better styling
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Style the notebook with CSS-like appearance
        style = ttk.Style()
        style.configure('TNotebook', background='#ffffff', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[25, 12], font=('Arial', 12, 'bold'),
                       background='#f3f4f6', foreground='#374151')
        style.map('TNotebook.Tab',
                 background=[('selected', '#3b82f6'), ('active', '#dbeafe')],
                 foreground=[('selected', '#ffffff'), ('active', '#1e40af')])
        
        # Login tab
        self.create_login_tab()
        
        # Signup tab
        self.create_signup_tab()
        
        # Clear any existing text and set focus
        self.clear_login_fields()
    
    def clear_login_fields(self):
        """Clear all login fields and set focus"""
        if hasattr(self, 'login_username'):
            self.login_username.delete(0, tk.END)
            self.login_username.focus_set()
        if hasattr(self, 'login_password'):
            self.login_password.delete(0, tk.END)
    
    def create_login_tab(self):
        """Create login tab with CSS-like styling"""
        login_frame = ttk.Frame(self.notebook)
        self.notebook.add(login_frame, text="🔐 Login")
        
        # Create scrollable frame for better UX
        canvas = tk.Canvas(login_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(login_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Login form with CSS-like styling
        form_frame = tk.Frame(scrollable_frame, bg='#ffffff')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Welcome message with modern styling
        welcome_label = tk.Label(form_frame, text="Welcome Back!", 
                                font=("Arial", 22, "bold"), bg='#ffffff', fg='#1f2937')
        welcome_label.pack(pady=(0, 40))
        
        # Username field with CSS-like styling
        username_frame = tk.Frame(form_frame, bg='#ffffff')
        username_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(username_frame, text="Username", font=("Arial", 14, "bold"), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 8))
        
        self.login_username = tk.Entry(username_frame, font=("Arial", 16), 
                                      relief='solid', bd=1, bg='#f9fafb', fg='#1f2937',
                                      insertbackground='#1f2937', selectbackground='#3b82f6',
                                      highlightthickness=1, highlightcolor='#3b82f6',
                                      highlightbackground='#d1d5db')
        self.login_username.pack(fill=tk.X, pady=(0, 0), ipady=12)
        
        # Password field with CSS-like styling
        password_frame = tk.Frame(form_frame, bg='#ffffff')
        password_frame.pack(fill=tk.X, pady=(0, 40))
        
        tk.Label(password_frame, text="Password", font=("Arial", 14, "bold"), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 8))
        
        self.login_password = tk.Entry(password_frame, font=("Arial", 16), show="•", 
                                      relief='solid', bd=1, bg='#f9fafb', fg='#1f2937',
                                      insertbackground='#1f2937', selectbackground='#3b82f6',
                                      highlightthickness=1, highlightcolor='#3b82f6',
                                      highlightbackground='#d1d5db')
        self.login_password.pack(fill=tk.X, pady=(0, 0), ipady=12)
        
        # Login button with modern CSS-like styling
        login_btn = tk.Button(form_frame, text="Sign In", font=("Arial", 16, "bold"),
                             bg='#059669', fg='white', relief='flat', 
                             padx=50, pady=15, cursor='hand2', command=self.login,
                             activebackground='#047857', activeforeground='white')
        login_btn.pack(pady=(0, 30))
        
        # Demo credentials with modern styling
        demo_frame = tk.Frame(form_frame, bg='#f8fafc', relief='flat', bd=1)
        demo_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(demo_frame, text="💡 Demo Account", font=("Arial", 13, "bold"), 
                bg='#f8fafc', fg='#374151').pack(pady=(20, 8))
        tk.Label(demo_frame, text="Username: admin", font=("Arial", 12), 
                bg='#f8fafc', fg='#6b7280').pack()
        tk.Label(demo_frame, text="Password: admin123", font=("Arial", 12), 
                bg='#f8fafc', fg='#6b7280').pack(pady=(0, 20))
        
        # Set focus to username field and bind Enter key
        self.login_username.focus_set()
        self.login_username.bind('<Return>', lambda e: self.login_password.focus_set())
        self.login_password.bind('<Return>', lambda e: self.login())
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_signup_tab(self):
        """Create signup tab with CSS-like styling"""
        signup_frame = ttk.Frame(self.notebook)
        self.notebook.add(signup_frame, text="📝 Sign Up")
        
        # Create scrollable frame for better UX
        canvas = tk.Canvas(signup_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(signup_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Signup form with CSS-like styling
        form_frame = tk.Frame(scrollable_frame, bg='#ffffff')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Welcome message with modern styling
        welcome_label = tk.Label(form_frame, text="Create Account", 
                                font=("Arial", 22, "bold"), bg='#ffffff', fg='#1f2937')
        welcome_label.pack(pady=(0, 40))
        
        # Full Name field with CSS-like styling
        name_frame = tk.Frame(form_frame, bg='#ffffff')
        name_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(name_frame, text="Full Name", font=("Arial", 14, "bold"), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 8))
        
        self.signup_fullname = tk.Entry(name_frame, font=("Arial", 16), 
                                       relief='solid', bd=1, bg='#f9fafb', fg='#1f2937',
                                       insertbackground='#1f2937', selectbackground='#3b82f6',
                                       highlightthickness=1, highlightcolor='#3b82f6',
                                       highlightbackground='#d1d5db')
        self.signup_fullname.pack(fill=tk.X, pady=(0, 0), ipady=12)
        
        # Username field with CSS-like styling
        username_frame = tk.Frame(form_frame, bg='#ffffff')
        username_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(username_frame, text="Username", font=("Arial", 14, "bold"), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 8))
        
        self.signup_username = tk.Entry(username_frame, font=("Arial", 16), 
                                       relief='solid', bd=1, bg='#f9fafb', fg='#1f2937',
                                       insertbackground='#1f2937', selectbackground='#3b82f6',
                                       highlightthickness=1, highlightcolor='#3b82f6',
                                       highlightbackground='#d1d5db')
        self.signup_username.pack(fill=tk.X, pady=(0, 0), ipady=12)
        
        # Email field with CSS-like styling
        email_frame = tk.Frame(form_frame, bg='#ffffff')
        email_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(email_frame, text="Email", font=("Arial", 14, "bold"), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 8))
        
        self.signup_email = tk.Entry(email_frame, font=("Arial", 16), 
                                    relief='solid', bd=1, bg='#f9fafb', fg='#1f2937',
                                    insertbackground='#1f2937', selectbackground='#3b82f6',
                                    highlightthickness=1, highlightcolor='#3b82f6',
                                    highlightbackground='#d1d5db')
        self.signup_email.pack(fill=tk.X, pady=(0, 0), ipady=12)
        
        # Password field with CSS-like styling
        password_frame = tk.Frame(form_frame, bg='#ffffff')
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(password_frame, text="Password", font=("Arial", 14, "bold"), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 8))
        
        self.signup_password = tk.Entry(password_frame, font=("Arial", 16), show="•", 
                                       relief='solid', bd=1, bg='#f9fafb', fg='#1f2937',
                                       insertbackground='#1f2937', selectbackground='#3b82f6',
                                       highlightthickness=1, highlightcolor='#3b82f6',
                                       highlightbackground='#d1d5db')
        self.signup_password.pack(fill=tk.X, pady=(0, 0), ipady=12)
        
        # Confirm Password field with CSS-like styling
        confirm_frame = tk.Frame(form_frame, bg='#ffffff')
        confirm_frame.pack(fill=tk.X, pady=(0, 40))
        
        tk.Label(confirm_frame, text="Confirm Password", font=("Arial", 14, "bold"), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 8))
        
        self.signup_confirm_password = tk.Entry(confirm_frame, font=("Arial", 16), show="•", 
                                               relief='solid', bd=1, bg='#f9fafb', fg='#1f2937',
                                               insertbackground='#1f2937', selectbackground='#3b82f6',
                                               highlightthickness=1, highlightcolor='#3b82f6',
                                               highlightbackground='#d1d5db')
        self.signup_confirm_password.pack(fill=tk.X, pady=(0, 0), ipady=12)
        
        # Signup button with modern CSS-like styling
        signup_btn = tk.Button(form_frame, text="Create Account", font=("Arial", 16, "bold"),
                               bg='#3b82f6', fg='white', relief='flat', 
                               padx=50, pady=15, cursor='hand2', command=self.signup,
                               activebackground='#2563eb', activeforeground='white')
        signup_btn.pack(pady=(0, 30))
        
        # Set focus to first field and bind Enter key for navigation
        self.signup_fullname.focus_set()
        self.signup_fullname.bind('<Return>', lambda e: self.signup_username.focus_set())
        self.signup_username.bind('<Return>', lambda e: self.signup_email.focus_set())
        self.signup_email.bind('<Return>', lambda e: self.signup_password.focus_set())
        self.signup_password.bind('<Return>', lambda e: self.signup_confirm_password.focus_set())
        self.signup_confirm_password.bind('<Return>', lambda e: self.signup())
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def login(self):
        """Handle login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            # Check credentials
            password_hash = self.hash_password(password)
            self.cursor.execute('''
                SELECT user_id, username, full_name, role FROM users 
                WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            
            user = self.cursor.fetchone()
            
            if user:
                messagebox.showinfo("Success", f"Welcome back, {user[2]}!")
                self.root.destroy()  # Close login window
                self.open_main_application(user)
            else:
                messagebox.showerror("Error", "Invalid username or password")
                
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def signup(self):
        """Handle signup"""
        fullname = self.signup_fullname.get().strip()
        username = self.signup_username.get().strip()
        email = self.signup_email.get().strip()
        password = self.signup_password.get()
        confirm_password = self.signup_confirm_password.get()
        
        # Validation
        if not all([fullname, username, email, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        try:
            # Check if username or email already exists
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ? OR email = ?", 
                              (username, email))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Username or email already exists")
                return
            
            # Create new user
            password_hash = self.hash_password(password)
            self.cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, fullname, 'user'))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Account created successfully! You can now login.")
            
            # Clear form
            self.signup_fullname.delete(0, tk.END)
            self.signup_username.delete(0, tk.END)
            self.signup_email.delete(0, tk.END)
            self.signup_password.delete(0, tk.END)
            self.signup_confirm_password.delete(0, tk.END)
            
            # Switch to login tab
            self.notebook.select(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Signup failed: {str(e)}")
    
    def open_main_application(self, user):
        """Open the main application after successful login"""
        try:
            # Import and create main application
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            
            from main import FarmerManagementSystem
            
            # Create new root window for main app
            main_root = tk.Tk()
            app = FarmerManagementSystem(main_root, user)
            app.run()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open main application: {str(e)}")
    
    def run(self):
        """Start the login window"""
        self.root.mainloop()

def main():
    """Main entry point for login"""
    root = tk.Tk()
    app = LoginWindow(root)
    app.run()

if __name__ == "__main__":
    main() 