import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib
# matplotlib.use('TkAgg')

class MainWindow:
    def __init__(self, root, farmer_manager, crop_manager, finance_manager, user=None):
        self.root = root
        self.farmer_manager = farmer_manager
        self.crop_manager = crop_manager
        self.finance_manager = finance_manager
        self.user = user
        
        self.setup_ui()
        self.load_dashboard_data()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header with user info
        self.create_header()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_farmers_tab()
        self.create_crops_tab()
        self.create_finance_tab()
        self.create_reports_tab()
        self.create_users_tab()  # Add users tab
    
    def create_header(self):
        """Create header with user information and logout button"""
        header_frame = tk.Frame(self.main_frame, bg='#1e40af', height=70)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Left side - User info
        user_frame = tk.Frame(header_frame, bg='#1e40af')
        user_frame.pack(side=tk.LEFT, padx=25, pady=20)
        
        if self.user:
            user_id, username, full_name, role = self.user
            tk.Label(user_frame, text=f"👤 {full_name}", 
                    font=("Arial", 14, "bold"), bg='#1e40af', fg='white').pack(side=tk.LEFT)
            tk.Label(user_frame, text=f"({role})", 
                    font=("Arial", 11), bg='#1e40af', fg='#bfdbfe').pack(side=tk.LEFT, padx=(8, 0))
        else:
            tk.Label(user_frame, text="👤 Guest User", 
                    font=("Arial", 14, "bold"), bg='#1e40af', fg='white').pack(side=tk.LEFT)
        
        # Right side - Logout button
        logout_frame = tk.Frame(header_frame, bg='#1e40af')
        logout_frame.pack(side=tk.RIGHT, padx=25, pady=20)
        
        logout_btn = tk.Button(logout_frame, text="🚪 Logout", 
                              font=("Arial", 11, "bold"), bg='#dc2626', fg='white',
                              relief='flat', padx=20, pady=8, cursor='hand2', command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Center - Title
        title_frame = tk.Frame(header_frame, bg='#1e40af')
        title_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(title_frame, text="🌾 Farmer Management System", 
                font=("Arial", 18, "bold"), bg='#1e40af', fg='white').pack(expand=True)
    
    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            # Restart with login
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from gui.login_window import LoginWindow
            root = tk.Tk()
            login_app = LoginWindow(root)
            login_app.run()
    
    def create_dashboard_tab(self):
        """Create the dashboard tab"""
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="📊 Dashboard")
        
        # Dashboard title with better styling
        title_frame = tk.Frame(self.dashboard_frame, bg='#f8fafc')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="Welcome to Farmer Management System", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=15)
        
        # Create dashboard content
        self.create_dashboard_content()
    
    def create_dashboard_content(self):
        """Create dashboard content with statistics"""
        # Statistics frame with better styling
        stats_frame = ttk.LabelFrame(self.dashboard_frame, text="📈 System Statistics", padding=15)
        stats_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Statistics labels with better styling
        self.total_farmers_label = ttk.Label(stats_frame, text="👥 Total Farmers: 0", 
                                            font=("Arial", 12))
        self.total_farmers_label.pack(anchor=tk.W, pady=5)
        
        self.total_crops_label = ttk.Label(stats_frame, text="🌱 Total Crops: 0", 
                                          font=("Arial", 12))
        self.total_crops_label.pack(anchor=tk.W, pady=5)
        
        self.active_plantings_label = ttk.Label(stats_frame, text="🌿 Active Plantings: 0", 
                                               font=("Arial", 12))
        self.active_plantings_label.pack(anchor=tk.W, pady=5)
        
        self.total_income_label = ttk.Label(stats_frame, text="💰 Total Income: ₹0", 
                                           font=("Arial", 12))
        self.total_income_label.pack(anchor=tk.W, pady=5)
        
        # Recent activities frame with better styling
        activities_frame = ttk.LabelFrame(self.dashboard_frame, text="📋 Recent Activities", padding=15)
        activities_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Activities treeview with better styling
        self.activities_tree = ttk.Treeview(activities_frame, columns=("Date", "Activity", "Details"), 
                                          show="headings", height=12)
        self.activities_tree.heading("Date", text="📅 Date")
        self.activities_tree.heading("Activity", text="📝 Activity")
        self.activities_tree.heading("Details", text="📄 Details")
        self.activities_tree.column("Date", width=120)
        self.activities_tree.column("Activity", width=150)
        self.activities_tree.column("Details", width=350)
        self.activities_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_farmers_tab(self):
        """Create the farmers management tab"""
        self.farmers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.farmers_frame, text="👥 Farmers")
        
        # Farmers management content
        self.create_farmers_content()
    
    def create_farmers_content(self):
        """Create farmers management content"""
        # Control frame
        control_frame = ttk.Frame(self.farmers_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add farmer button
        add_btn = ttk.Button(control_frame, text="➕ Add Farmer", command=self.add_farmer_dialog)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.farmer_search_var = tk.StringVar()
        self.farmer_search_var.trace('w', self.search_farmers)
        search_entry = ttk.Entry(search_frame, textvariable=self.farmer_search_var)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Farmers treeview
        tree_frame = ttk.Frame(self.farmers_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.farmers_tree = ttk.Treeview(tree_frame, 
                                       columns=("ID", "Name", "Phone", "Email", "Farm Size"),
                                       show="headings", height=15)
        self.farmers_tree.heading("ID", text="🆔 ID")
        self.farmers_tree.heading("Name", text="👤 Name")
        self.farmers_tree.heading("Phone", text="📞 Phone")
        self.farmers_tree.heading("Email", text="📧 Email")
        self.farmers_tree.heading("Farm Size", text="📏 Farm Size (acres)")
        
        self.farmers_tree.column("ID", width=50)
        self.farmers_tree.column("Name", width=150)
        self.farmers_tree.column("Phone", width=120)
        self.farmers_tree.column("Email", width=200)
        self.farmers_tree.column("Farm Size", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.farmers_tree.yview)
        self.farmers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.farmers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click for editing
        self.farmers_tree.bind("<Double-1>", self.edit_farmer)
        
        # Load farmers data
        self.load_farmers_data()
    
    def create_crops_tab(self):
        """Create the crops management tab"""
        self.crops_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.crops_frame, text="🌱 Crops & Plantings")
        
        # Create notebook for crops and plantings
        crops_notebook = ttk.Notebook(self.crops_frame)
        crops_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crops tab
        self.create_crops_content(crops_notebook)
        
        # Plantings tab
        self.create_plantings_content(crops_notebook)
    
    def create_crops_content(self, parent):
        """Create crops management content"""
        crops_frame = ttk.Frame(parent)
        parent.add(crops_frame, text="🌾 Crops")
        
        # Control frame
        control_frame = ttk.Frame(crops_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_crop_btn = ttk.Button(control_frame, text="➕ Add Crop", command=self.add_crop_dialog)
        add_crop_btn.pack(side=tk.LEFT, padx=5)
        
        # Crops treeview
        tree_frame = ttk.Frame(crops_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.crops_tree = ttk.Treeview(tree_frame, 
                                      columns=("ID", "Name", "Variety", "Growth Period", "Yield/Acre", "Price"),
                                      show="headings", height=15)
        self.crops_tree.heading("ID", text="🆔 ID")
        self.crops_tree.heading("Name", text="🌾 Crop Name")
        self.crops_tree.heading("Variety", text="🌿 Variety")
        self.crops_tree.heading("Growth Period", text="⏱️ Growth Period (days)")
        self.crops_tree.heading("Yield/Acre", text="📊 Yield/Acre")
        self.crops_tree.heading("Price", text="💰 Price/Unit")
        
        self.crops_tree.column("ID", width=50)
        self.crops_tree.column("Name", width=150)
        self.crops_tree.column("Variety", width=100)
        self.crops_tree.column("Growth Period", width=120)
        self.crops_tree.column("Yield/Acre", width=100)
        self.crops_tree.column("Price", width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.crops_tree.yview)
        self.crops_tree.configure(yscrollcommand=scrollbar.set)
        
        self.crops_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_crops_data()
    
    def create_plantings_content(self, parent):
        """Create plantings management content"""
        plantings_frame = ttk.Frame(parent)
        parent.add(plantings_frame, text="🌱 Plantings")
        
        # Control frame
        control_frame = ttk.Frame(plantings_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_planting_btn = ttk.Button(control_frame, text="➕ Add Planting", command=self.add_planting_dialog)
        add_planting_btn.pack(side=tk.LEFT, padx=5)
        
        # Plantings treeview
        tree_frame = ttk.Frame(plantings_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.plantings_tree = ttk.Treeview(tree_frame, 
                                         columns=("ID", "Farmer", "Crop", "Planting Date", "Area", "Harvest Date", "Status"),
                                         show="headings", height=15)
        self.plantings_tree.heading("ID", text="🆔 ID")
        self.plantings_tree.heading("Farmer", text="👤 Farmer")
        self.plantings_tree.heading("Crop", text="🌾 Crop")
        self.plantings_tree.heading("Planting Date", text="📅 Planting Date")
        self.plantings_tree.heading("Area", text="📏 Area (acres)")
        self.plantings_tree.heading("Harvest Date", text="🌾 Expected Harvest")
        self.plantings_tree.heading("Status", text="📊 Status")
        
        self.plantings_tree.column("ID", width=50)
        self.plantings_tree.column("Farmer", width=150)
        self.plantings_tree.column("Crop", width=100)
        self.plantings_tree.column("Planting Date", width=100)
        self.plantings_tree.column("Area", width=80)
        self.plantings_tree.column("Harvest Date", width=100)
        self.plantings_tree.column("Status", width=80)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.plantings_tree.yview)
        self.plantings_tree.configure(yscrollcommand=scrollbar.set)
        
        self.plantings_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_plantings_data()
    
    def create_finance_tab(self):
        """Create the finance management tab"""
        self.finance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.finance_frame, text="💰 Finance")
        
        # Finance content
        self.create_finance_content()
    
    def create_finance_content(self):
        """Create finance management content"""
        # Control frame
        control_frame = ttk.Frame(self.finance_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_transaction_btn = ttk.Button(control_frame, text="➕ Add Transaction", command=self.add_transaction_dialog)
        add_transaction_btn.pack(side=tk.LEFT, padx=5)
        
        # Summary frame with better styling
        summary_frame = ttk.LabelFrame(self.finance_frame, text="💰 Financial Summary", padding=15)
        summary_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.total_income_summary = ttk.Label(summary_frame, text="💵 Total Income: ₹0", font=("Arial", 12))
        self.total_income_summary.pack(anchor=tk.W, pady=5)
        
        self.total_expenses_summary = ttk.Label(summary_frame, text="💸 Total Expenses: ₹0", font=("Arial", 12))
        self.total_expenses_summary.pack(anchor=tk.W, pady=5)
        
        self.net_profit_summary = ttk.Label(summary_frame, text="📈 Net Profit: ₹0", font=("Arial", 12))
        self.net_profit_summary.pack(anchor=tk.W, pady=5)
        
        # Transactions treeview
        tree_frame = ttk.Frame(self.finance_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.transactions_tree = ttk.Treeview(tree_frame, 
                                            columns=("ID", "Farmer", "Type", "Category", "Amount", "Date", "Description"),
                                            show="headings", height=15)
        self.transactions_tree.heading("ID", text="🆔 ID")
        self.transactions_tree.heading("Farmer", text="👤 Farmer")
        self.transactions_tree.heading("Type", text="📊 Type")
        self.transactions_tree.heading("Category", text="🏷️ Category")
        self.transactions_tree.heading("Amount", text="💰 Amount")
        self.transactions_tree.heading("Date", text="📅 Date")
        self.transactions_tree.heading("Description", text="📄 Description")
        
        self.transactions_tree.column("ID", width=50)
        self.transactions_tree.column("Farmer", width=150)
        self.transactions_tree.column("Type", width=80)
        self.transactions_tree.column("Category", width=100)
        self.transactions_tree.column("Amount", width=100)
        self.transactions_tree.column("Date", width=100)
        self.transactions_tree.column("Description", width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_transactions_data()
    
    def create_reports_tab(self):
        """Create the reports tab"""
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="📊 Reports")
        
        # Reports content
        self.create_reports_content()
    
    def create_reports_content(self):
        """Create reports content"""
        # Reports notebook
        reports_notebook = ttk.Notebook(self.reports_frame)
        reports_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Financial reports
        self.create_financial_reports(reports_notebook)
        
        # Crop reports
        self.create_crop_reports(reports_notebook)
    
    def create_financial_reports(self, parent):
        """Create financial reports"""
        finance_reports_frame = ttk.Frame(parent)
        parent.add(finance_reports_frame, text="💰 Financial Reports")
        
        # Simple text report instead of chart
        report_frame = ttk.Frame(finance_reports_frame)
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.financial_report_text = tk.Text(report_frame, wrap=tk.WORD, height=20, 
                                           font=("Consolas", 10), bg='#f8fafc')
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.financial_report_text.yview)
        self.financial_report_text.configure(yscrollcommand=scrollbar.set)
        
        self.financial_report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_financial_report()
    
    def create_crop_reports(self, parent):
        """Create crop reports"""
        crop_reports_frame = ttk.Frame(parent)
        parent.add(crop_reports_frame, text="🌱 Crop Reports")
        
        # Simple text report instead of chart
        report_frame = ttk.Frame(crop_reports_frame)
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.crop_report_text = tk.Text(report_frame, wrap=tk.WORD, height=20, 
                                       font=("Consolas", 10), bg='#f8fafc')
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.crop_report_text.yview)
        self.crop_report_text.configure(yscrollcommand=scrollbar.set)
        
        self.crop_report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_crop_report()
    
    # Data loading methods
    def load_dashboard_data(self):
        """Load dashboard data"""
        try:
            # Get statistics
            farmers = self.farmer_manager.get_all_farmers()
            crops = self.crop_manager.get_all_crops()
            plantings = self.crop_manager.get_all_plantings()
            financial_summary = self.finance_manager.get_financial_summary()
            
            # Update labels
            self.total_farmers_label.config(text=f"👥 Total Farmers: {len(farmers)}")
            self.total_crops_label.config(text=f"🌱 Total Crops: {len(crops)}")
            
            active_plantings = [p for p in plantings if p['status'] == 'Growing']
            self.active_plantings_label.config(text=f"🌿 Active Plantings: {len(active_plantings)}")
            
            self.total_income_label.config(text=f"💰 Total Income: ₹{financial_summary['total_income']:,.2f}")
            
            # Load recent activities
            self.load_recent_activities()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dashboard data: {str(e)}")
    
    def load_farmers_data(self):
        """Load farmers data into treeview"""
        try:
            # Clear existing items
            for item in self.farmers_tree.get_children():
                self.farmers_tree.delete(item)
            
            # Get farmers data
            farmers = self.farmer_manager.get_all_farmers()
            
            # Insert data
            for farmer in farmers:
                self.farmers_tree.insert("", "end", values=(
                    farmer['farmer_id'],
                    farmer['name'],
                    farmer['phone'] or "",
                    farmer['email'] or "",
                    f"{farmer['farm_size']:.1f}" if farmer['farm_size'] else ""
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load farmers data: {str(e)}")
    
    def load_crops_data(self):
        """Load crops data into treeview"""
        try:
            # Clear existing items
            for item in self.crops_tree.get_children():
                self.crops_tree.delete(item)
            
            # Get crops data
            crops = self.crop_manager.get_all_crops()
            
            # Insert data
            for crop in crops:
                self.crops_tree.insert("", "end", values=(
                    crop['crop_id'],
                    crop['name'],
                    crop['variety'] or "",
                    crop['growth_period'] or "",
                    f"{crop['yield_per_acre']:.1f}" if crop['yield_per_acre'] else "",
                    f"₹{crop['price_per_unit']:.2f}" if crop['price_per_unit'] else ""
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load crops data: {str(e)}")
    
    def load_plantings_data(self):
        """Load plantings data into treeview"""
        try:
            # Clear existing items
            for item in self.plantings_tree.get_children():
                self.plantings_tree.delete(item)
            
            # Get plantings data
            plantings = self.crop_manager.get_all_plantings()
            
            # Insert data
            for planting in plantings:
                self.plantings_tree.insert("", "end", values=(
                    planting['planting_id'],
                    planting['farmer_name'],
                    planting['crop_name'],
                    planting['planting_date'],
                    f"{planting['area_planted']:.1f}",
                    planting['expected_harvest_date'],
                    planting['status']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load plantings data: {str(e)}")
    
    def load_transactions_data(self):
        """Load transactions data into treeview"""
        try:
            # Clear existing items
            for item in self.transactions_tree.get_children():
                self.transactions_tree.delete(item)
            
            # Get transactions data
            transactions = self.finance_manager.get_transactions()
            
            # Update summary
            summary = self.finance_manager.get_financial_summary()
            self.total_income_summary.config(text=f"💵 Total Income: ₹{summary['total_income']:,.2f}")
            self.total_expenses_summary.config(text=f"💸 Total Expenses: ₹{summary['total_expenses']:,.2f}")
            self.net_profit_summary.config(text=f"📈 Net Profit: ₹{summary['net_profit']:,.2f}")
            
            # Insert data
            for transaction in transactions:
                self.transactions_tree.insert("", "end", values=(
                    transaction['transaction_id'],
                    transaction['farmer_name'],
                    transaction['type'].title(),
                    transaction['category'],
                    f"₹{transaction['amount']:.2f}",
                    transaction['date'],
                    transaction['description'] or ""
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions data: {str(e)}")
    
    def load_recent_activities(self):
        """Load recent activities into treeview"""
        try:
            # Clear existing items
            for item in self.activities_tree.get_children():
                self.activities_tree.delete(item)
            
            # Get recent transactions
            recent_transactions = self.finance_manager.get_transactions()
            for transaction in recent_transactions[:10]:  # Show last 10
                self.activities_tree.insert("", "end", values=(
                    transaction['date'],
                    f"{transaction['type'].title()} Transaction",
                    f"{transaction['farmer_name']} - {transaction['category']} - ₹{transaction['amount']:.2f}"
                ))
                
        except Exception as e:
            print(f"Failed to load recent activities: {str(e)}")
    
    # Dialog methods (to be implemented)
    def add_farmer_dialog(self):
        """Show add farmer dialog"""
        messagebox.showinfo("Info", "Add Farmer dialog will be implemented")
    
    def edit_farmer(self, event):
        """Edit selected farmer"""
        selection = self.farmers_tree.selection()
        if selection:
            messagebox.showinfo("Info", "Edit Farmer dialog will be implemented")
    
    def search_farmers(self, *args):
        """Search farmers based on search term"""
        search_term = self.farmer_search_var.get()
        if search_term:
            try:
                # Clear existing items
                for item in self.farmers_tree.get_children():
                    self.farmers_tree.delete(item)
                
                # Search farmers
                farmers = self.farmer_manager.search_farmers(search_term)
                
                # Insert results
                for farmer in farmers:
                    self.farmers_tree.insert("", "end", values=(
                        farmer['farmer_id'],
                        farmer['name'],
                        farmer['phone'] or "",
                        farmer['email'] or "",
                        f"{farmer['farm_size']:.1f}" if farmer['farm_size'] else ""
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
        else:
            # Reload all farmers
            self.load_farmers_data()
    
    def add_crop_dialog(self):
        """Show add crop dialog"""
        messagebox.showinfo("Info", "Add Crop dialog will be implemented")
    
    def add_planting_dialog(self):
        """Show add planting dialog"""
        messagebox.showinfo("Info", "Add Planting dialog will be implemented")
    
    def add_transaction_dialog(self):
        """Show add transaction dialog"""
        messagebox.showinfo("Info", "Add Transaction dialog will be implemented")
    
    def update_financial_report(self):
        """Update financial report text"""
        try:
            self.financial_report_text.delete(1.0, tk.END)
            
            # Get monthly data
            monthly_data = self.finance_manager.get_monthly_summary()
            
            report_text = "Financial Summary Report\n"
            report_text += "=" * 50 + "\n\n"
            
            if monthly_data:
                report_text += "Monthly Financial Summary:\n"
                report_text += "-" * 30 + "\n"
                for row in monthly_data:
                    report_text += f"Month {row['month']}: Income ₹{row['monthly_income']:,.2f}, Expenses ₹{row['monthly_expenses']:,.2f}, Profit ₹{row['monthly_profit']:,.2f}\n"
            else:
                report_text += "No financial data available.\n"
            
            self.financial_report_text.insert(tk.END, report_text)
            
        except Exception as e:
            print(f"Failed to update financial report: {str(e)}")
    
    def update_crop_report(self):
        """Update crop report text"""
        try:
            self.crop_report_text.delete(1.0, tk.END)
            
            # Get crop statistics
            crop_stats = self.crop_manager.get_crop_statistics()
            
            report_text = "Crop Planting Report\n"
            report_text += "=" * 50 + "\n\n"
            
            if crop_stats['crop_stats']:
                report_text += "Plantings by Crop:\n"
                report_text += "-" * 20 + "\n"
                for row in crop_stats['crop_stats']:
                    total_area = row['total_area'] if row['total_area'] is not None else 0
                    report_text += f"{row['crop_name']}: {row['total_plantings']} plantings, {total_area:.1f} acres\n"
            else:
                report_text += "No crop data available.\n"
            
            self.crop_report_text.insert(tk.END, report_text)
            
        except Exception as e:
            print(f"Failed to update crop report: {str(e)}") 

    def create_users_tab(self):
        """Create the users management tab"""
        self.users_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.users_frame, text="👤 Users")
        
        # Users management content
        self.create_users_content()
    
    def create_users_content(self):
        """Create users management content"""
        # Control frame
        control_frame = ttk.Frame(self.users_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add user button (only for admin)
        if self.user and self.user[3] == 'admin':
            add_user_btn = ttk.Button(control_frame, text="➕ Add User", command=self.add_user_dialog)
            add_user_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.user_search_var = tk.StringVar()
        self.user_search_var.trace('w', self.search_users)
        search_entry = ttk.Entry(search_frame, textvariable=self.user_search_var)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Users treeview
        tree_frame = ttk.Frame(self.users_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.users_tree = ttk.Treeview(tree_frame, 
                                      columns=("ID", "Username", "Full Name", "Email", "Role", "Created Date"),
                                      show="headings", height=15)
        self.users_tree.heading("ID", text="🆔 ID")
        self.users_tree.heading("Username", text="👤 Username")
        self.users_tree.heading("Full Name", text="📝 Full Name")
        self.users_tree.heading("Email", text="📧 Email")
        self.users_tree.heading("Role", text="🔐 Role")
        self.users_tree.heading("Created Date", text="📅 Created Date")
        
        self.users_tree.column("ID", width=50)
        self.users_tree.column("Username", width=120)
        self.users_tree.column("Full Name", width=150)
        self.users_tree.column("Email", width=200)
        self.users_tree.column("Role", width=80)
        self.users_tree.column("Created Date", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click for editing (only for admin)
        if self.user and self.user[3] == 'admin':
            self.users_tree.bind("<Double-1>", self.edit_user)
        
        # Load users data
        self.load_users_data()
    
    def load_users_data(self):
        """Load users data into treeview"""
        try:
            # Clear existing items
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Get users data from database
            import sqlite3
            conn = sqlite3.connect('farm_management.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, username, full_name, email, role, created_date 
                FROM users 
                ORDER BY user_id
            ''')
            
            users = cursor.fetchall()
            conn.close()
            
            # Insert data
            for user in users:
                # Format the created date
                created_date = user[5] if user[5] else "N/A"
                if created_date != "N/A":
                    try:
                        # Parse and format the date
                        from datetime import datetime
                        dt = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                        created_date = dt.strftime('%Y-%m-%d %H:%M')
                    except:
                        created_date = "N/A"
                
                self.users_tree.insert("", "end", values=(
                    user[0],  # ID
                    user[1],  # Username
                    user[2] or "",  # Full Name
                    user[3] or "",  # Email
                    user[4] or "user",  # Role
                    created_date  # Created Date
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users data: {str(e)}")
    
    def search_users(self, *args):
        """Search users based on search term"""
        search_term = self.user_search_var.get().lower()
        if search_term:
            try:
                # Clear existing items
                for item in self.users_tree.get_children():
                    self.users_tree.delete(item)
                
                # Search users in database
                import sqlite3
                conn = sqlite3.connect('farm_management.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT user_id, username, full_name, email, role, created_date 
                    FROM users 
                    WHERE LOWER(username) LIKE ? OR LOWER(full_name) LIKE ? OR LOWER(email) LIKE ?
                    ORDER BY user_id
                ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                
                users = cursor.fetchall()
                conn.close()
                
                # Insert results
                for user in users:
                    created_date = user[5] if user[5] else "N/A"
                    if created_date != "N/A":
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                            created_date = dt.strftime('%Y-%m-%d %H:%M')
                        except:
                            created_date = "N/A"
                    
                    self.users_tree.insert("", "end", values=(
                        user[0], user[1], user[2] or "", user[3] or "", 
                        user[4] or "user", created_date
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
        else:
            # Reload all users
            self.load_users_data()
    
    def add_user_dialog(self):
        """Show add user dialog (admin only)"""
        if not self.user or self.user[3] != 'admin':
            messagebox.showerror("Error", "Only administrators can add users")
            return
        
        messagebox.showinfo("Info", "Add User dialog will be implemented")
    
    def edit_user(self, event):
        """Edit selected user (admin only)"""
        if not self.user or self.user[3] != 'admin':
            messagebox.showerror("Error", "Only administrators can edit users")
            return
        
        selection = self.users_tree.selection()
        if selection:
            messagebox.showinfo("Info", "Edit User dialog will be implemented") 