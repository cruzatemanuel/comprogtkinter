import os

SESSION_FILE = "session.txt"

def save_session(srcode):
    """Save SRCODE to session file"""
    try:
        with open(SESSION_FILE, 'w') as f:
            f.write(srcode)
        return True
    except Exception as e:
        print(f"Error saving session: {e}")
        return False

def load_session():
    """Load SRCODE from session file"""
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                srcode = f.read().strip()
                return srcode if srcode else None
        return None
    except Exception as e:
        print(f"Error loading session: {e}")
        return None

def clear_session():
    """Delete session file"""
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        return True
    except Exception as e:
        print(f"Error clearing session: {e}")
        return False

