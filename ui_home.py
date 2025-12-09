import tkinter as tk
from tkinter import ttk

def create_home_page(parent, navigate_callback):
    """Create and return the Home page widget"""
    frame = tk.Frame(parent, bg='#f0f0f0')
    
    # Main content area
    content_frame = tk.Frame(frame, bg='#f0f0f0', padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Program description
    title_label = tk.Label(
        content_frame,
        text="Fare Tracker Application",
        font=('Arial', 24, 'bold'),
        bg='#f0f0f0',
        fg='#333'
    )
    title_label.pack(pady=(0, 20))
    
    description_text = """
Welcome to the Fare Tracker Application!

This application helps you track and calculate transportation fares
for various routes in Batangas. You can:

• Calculate fares for different routes across 6 districts
• Track your fare history and expenses
• View weekly averages of your transportation costs
• Manage your profile and update your information

Use the navigation tabs above to explore the different features
of the application.
    """
    
    desc_label = tk.Label(
        content_frame,
        text=description_text,
        font=('Arial', 12),
        bg='#f0f0f0',
        fg='#555',
        justify=tk.LEFT,
        anchor='w'
    )
    desc_label.pack(pady=10, padx=20)
    
    # Footer with navigation links
    footer_frame = tk.Frame(frame, bg='#e0e0e0', height=50)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    footer_frame.pack_propagate(False)
    
    footer_label = tk.Label(
        footer_frame,
        text="Navigation: ",
        font=('Arial', 10),
        bg='#e0e0e0',
        fg='#333'
    )
    footer_label.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Navigation links (styled as clickable labels)
    links = [
        ("Home", "home"),
        ("Track", "track"),
        ("My Dashboard", "dashboard"),
        ("Logout", "logout")
    ]
    
    for link_text, page in links:
        link = tk.Label(
            footer_frame,
            text=link_text,
            font=('Arial', 10, 'underline'),
            bg='#e0e0e0',
            fg='#0066cc',
            cursor='hand2'
        )
        link.pack(side=tk.LEFT, padx=5)
        link.bind('<Button-1>', lambda e, p=page: navigate_callback(p))
    
    return frame

