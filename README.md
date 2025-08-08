# Farmer Management System

A comprehensive database management system for agricultural operations built with Python and SQLite, featuring user authentication and modern UI.

## 🌟 New Features

### 🔐 User Authentication System
- **Secure Login/Signup**: Modern authentication with password hashing
- **User Management**: Create accounts, manage roles (admin/user)
- **Session Management**: User-specific sessions with logout functionality
- **Demo Credentials**: Pre-configured admin account for testing

### 🎨 Beautiful Modern UI
- **Professional Design**: Clean, modern interface with proper styling
- **Responsive Layout**: Well-organized tabs and sections
- **User Information**: Display current user and role in header
- **Logout Functionality**: Secure logout with confirmation

## Features

### Core Modules
- **Farmer Management**: Registration, profiles, contact information
- **Crop Management**: Planting schedules, growth tracking, yield records
- **Equipment Management**: Tools, machinery, maintenance schedules
- **Financial Tracking**: Income, expenses, profit/loss analysis
- **Inventory Management**: Seeds, fertilizers, pesticides
- **Weather Integration**: Weather data for planning
- **Reports & Analytics**: Comprehensive reporting system

### DBMS Concepts Implemented
- Database design and normalization
- CRUD operations (Create, Read, Update, Delete)
- Complex SQL queries and joins
- Data relationships (One-to-Many, Many-to-Many)
- Data validation and constraints
- Backup and recovery procedures
- **User Authentication & Authorization**

## Technology Stack
- **Backend**: Python 3.8+
- **Database**: SQLite3
- **GUI**: tkinter (built-in Python GUI)
- **Authentication**: SHA-256 password hashing
- **Data Processing**: pandas, numpy
- **Charts**: matplotlib

## Installation

1. Ensure Python 3.8+ is installed
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🚀 Quick Start (with Login)
```bash
python run_app.py
```

### 🔧 Direct Access (without Login)
```bash
python main.py --no-login
```

### 📊 Demo Credentials
- **Username**: admin
- **Password**: admin123
- **Role**: System Administrator

## Database Schema

### Core Tables
- `users`: User accounts and authentication
- `farmers`: Farmer information and profiles
- `crops`: Crop types and varieties
- `plantings`: Planting records and schedules
- `equipment`: Farm equipment and tools
- `inventory`: Stock management
- `transactions`: Financial records
- `weather_data`: Weather information

## Project Structure
```
farmr_management/
├── run_app.py              # Main launcher with login
├── main.py                 # Direct application entry point
├── test_system.py          # System test script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── SETUP.md               # Setup guide
├── database/
│   ├── __init__.py
│   └── db_manager.py      # Database connection and setup
├── modules/
│   ├── __init__.py
│   ├── farmer.py          # Farmer management module
│   ├── crop.py            # Crop management module
│   └── finance.py         # Financial tracking module
├── gui/
│   ├── __init__.py
│   ├── login_window.py    # Login and signup interface
│   └── main_window.py     # Main application window
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Utility functions
└── data/
    ├── __init__.py
    └── sample_data.py     # Sample data for testing
```

## Authentication Features

### 🔐 Login System
- **Secure Password Hashing**: SHA-256 encryption
- **Email Validation**: Proper email format checking
- **User Roles**: Admin and regular user roles
- **Session Management**: User-specific sessions

### 📝 Signup System
- **Account Creation**: New user registration
- **Validation**: Username, email, password validation
- **Duplicate Prevention**: Check for existing users
- **Password Confirmation**: Double password entry

### 👤 User Management
- **User Profiles**: Display user information
- **Role-based Access**: Different permissions per role
- **Logout Functionality**: Secure session termination
- **Session Persistence**: Maintain user state

## Learning Objectives

This project demonstrates:
1. **Database Design**: Proper table structure and relationships
2. **SQL Operations**: Complex queries, joins, aggregations
3. **Data Integrity**: Constraints, validation, normalization
4. **Application Development**: GUI development with database backend
5. **Authentication Systems**: User management and security
6. **Real-world Application**: Practical business logic implementation

## Security Features

- **Password Hashing**: SHA-256 encryption for secure storage
- **Input Validation**: Comprehensive form validation
- **SQL Injection Prevention**: Parameterized queries
- **Session Management**: Secure user sessions
- **Role-based Access**: Different user permissions

## Contributing

This is an educational project. Feel free to extend functionality or improve the code structure.

## Academic Use

This project is perfect for:
- **DBMS coursework**: Demonstrates all major database concepts
- **Software Engineering**: Shows proper project structure and design
- **Python Programming**: Covers GUI, database, and data analysis
- **Security Concepts**: Authentication and authorization systems
- **Business Applications**: Real-world agricultural management system 