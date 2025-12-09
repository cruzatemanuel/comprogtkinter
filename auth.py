from database import create_user, get_user
from session import save_session

def signup(srcode, name, password, college):
    """Handle user signup"""
    # Validate inputs
    if not srcode or not name or not password or not college:
        return False, "All fields are required"
    
    # Check if user already exists
    existing_user = get_user(srcode)
    if existing_user:
        return False, "SRCODE already exists"
    
    # Create user
    if create_user(srcode, name, password, college):
        # Auto-login: save session
        save_session(srcode)
        return True, "Signup successful"
    else:
        return False, "Error creating user. Please check database connection."

def login(srcode, password):
    """Handle user login"""
    # Validate inputs
    if not srcode or not password:
        return False, None, "SRCODE and password are required"
    
    # Get user from database
    user = get_user(srcode)
    if not user:
        return False, None, "Invalid SRCODE or password"
    
    # Check password (plain text comparison)
    if user.get('password') != password:
        return False, None, "Invalid SRCODE or password"
    
    # Save session
    save_session(srcode)
    return True, user, "Login successful"

