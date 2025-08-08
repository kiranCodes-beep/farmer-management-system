import re
from datetime import datetime, date
from typing import Optional, Union

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return True  # Empty email is allowed
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if not phone:
        return True  # Empty phone is allowed
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    return len(digits_only) >= 10

def validate_date(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD)"""
    if not date_str:
        return False
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_positive_number(value: Union[str, float, int]) -> bool:
    """Validate that a value is a positive number"""
    try:
        num = float(value)
        return num >= 0
    except (ValueError, TypeError):
        return False

def format_currency(amount):
    """Format amount as currency with rupee symbol"""
    if amount is None:
        return "₹0.00"
    return f"₹{amount:,.2f}"

def format_percentage(value, total):
    """Format value as percentage"""
    if total == 0:
        return "0.00%"
    percentage = (value / total) * 100
    return f"{percentage:.2f}%"

def calculate_age(birth_date: str) -> int:
    """Calculate age from birth date"""
    try:
        birth = datetime.strptime(birth_date, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth.year
        if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
            age -= 1
        return age
    except ValueError:
        return 0

def get_season_from_date(date_str: str) -> str:
    """Get season from date"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        month = date_obj.month
        
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"
    except ValueError:
        return "Unknown"

def calculate_days_between(start_date: str, end_date: str) -> int:
    """Calculate days between two dates"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return (end - start).days
    except ValueError:
        return 0

def is_future_date(date_str: str) -> bool:
    """Check if date is in the future"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        return date_obj > date.today()
    except ValueError:
        return False

def is_past_date(date_str: str) -> bool:
    """Check if date is in the past"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        return date_obj < date.today()
    except ValueError:
        return False

def get_current_date() -> str:
    """Get current date in YYYY-MM-DD format"""
    return date.today().strftime('%Y-%m-%d')

def get_date_range(days_back: int = 30) -> tuple[str, str]:
    """Get date range from today going back N days"""
    end_date = date.today()
    start_date = end_date - datetime.timedelta(days=days_back)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent SQL injection"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def generate_unique_id() -> str:
    """Generate a unique identifier"""
    import uuid
    return str(uuid.uuid4())[:8]

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension"""
    if not filename:
        return False
    
    file_extension = filename.lower().split('.')[-1]
    return file_extension in allowed_extensions 