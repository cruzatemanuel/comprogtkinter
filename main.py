import tkinter as tk
from tkinter import ttk, messagebox
from database import initialize_database
from session import load_session, clear_session
from auth import signup, login
from ui_home import create_home_page
from ui_track import TrackPage
from ui_dashboard import DashboardPage

class FareTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fare Tracker Application")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        initialize_database()
        
        # Current page
        self.current_page = None
        self.current_page_widget = None
        
        # Check if user is logged in
        self.check_session()
    
    def check_session(self):
        """Check if user has active session"""
        srcode = load_session()
        if srcode:
            self.show_main_app()
        else:
            self.show_auth_page()
    
    def show_auth_page(self):
        """Show authentication page (login/signup)"""
        self.clear_page()
        
        # Create auth frame
        auth_frame = tk.Frame(self.root, bg='#f0f0f0')
        auth_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            auth_frame,
            text="Fare Tracker",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=50)
        
        # Auth container
        container = tk.Frame(auth_frame, bg='#ffffff', padx=30, pady=30)
        container.pack(expand=True)
        
        # Tab selection
        self.auth_mode = tk.StringVar(value="login")
        
        login_radio = tk.Radiobutton(
            container,
            text="Login",
            variable=self.auth_mode,
            value="login",
            font=('Arial', 12),
            bg='#ffffff',
            command=self.switch_auth_mode
        )
        login_radio.pack(side=tk.LEFT, padx=10)
        
        signup_radio = tk.Radiobutton(
            container,
            text="Sign Up",
            variable=self.auth_mode,
            value="signup",
            font=('Arial', 12),
            bg='#ffffff',
            command=self.switch_auth_mode
        )
        signup_radio.pack(side=tk.LEFT, padx=10)
        
        # Form fields
        fields_frame = tk.Frame(container, bg='#ffffff')
        fields_frame.pack(pady=20)
        
        # SRCODE
        tk.Label(
            fields_frame,
            text="SRCODE:",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, pady=5)
        self.srcode_entry = tk.Entry(fields_frame, font=('Arial', 11), width=30)
        self.srcode_entry.pack(pady=5)
        
        # Name (only for signup)
        self.name_label = tk.Label(
            fields_frame,
            text="Name:",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        )
        self.name_entry = tk.Entry(fields_frame, font=('Arial', 11), width=30)
        
        # Password
        tk.Label(
            fields_frame,
            text="Password:",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, pady=5)
        self.password_entry = tk.Entry(fields_frame, font=('Arial', 11), width=30, show='*')
        self.password_entry.pack(pady=5)
        
        # College (only for signup)
        self.college_label = tk.Label(
            fields_frame,
            text="College:",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        )
        self.college_entry = tk.Entry(fields_frame, font=('Arial', 11), width=30)
        
        # Submit button
        submit_btn = tk.Button(
            container,
            text="Submit",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            command=self.handle_auth,
            padx=30,
            pady=10
        )
        submit_btn.pack(pady=20)
        
        # Initialize auth mode
        self.switch_auth_mode()
        
        self.current_page_widget = auth_frame
    
    def switch_auth_mode(self):
        """Switch between login and signup modes"""
        mode = self.auth_mode.get()
        
        if mode == "signup":
            # Show name and college fields
            self.name_label.pack(fill=tk.X, pady=5, before=self.password_entry)
            self.name_entry.pack(pady=5, before=self.password_entry)
            self.college_label.pack(fill=tk.X, pady=5, after=self.password_entry)
            self.college_entry.pack(pady=5, after=self.password_entry)
        else:
            # Hide name and college fields
            self.name_label.pack_forget()
            self.name_entry.pack_forget()
            self.college_label.pack_forget()
            self.college_entry.pack_forget()
    
    def handle_auth(self):
        """Handle login or signup"""
        srcode = self.srcode_entry.get().strip()
        password = self.password_entry.get().strip()
        
        mode = self.auth_mode.get()
        
        if mode == "login":
            if not srcode or not password:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            success, user, message = login(srcode, password)
            if success:
                messagebox.showinfo("Success", message)
                self.show_main_app()
            else:
                messagebox.showerror("Error", message)
        else:
            # Signup
            name = self.name_entry.get().strip()
            college = self.college_entry.get().strip()
            
            if not all([srcode, name, password, college]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            success, message = signup(srcode, name, password, college)
            if success:
                messagebox.showinfo("Success", message)
                self.show_main_app()
            else:
                messagebox.showerror("Error", message)
    
    def show_main_app(self):
        """Show main application with navigation"""
        self.clear_page()
        
        # Create main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Navigation bar
        nav_frame = tk.Frame(main_container, bg='#333', height=50)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)
        
        nav_buttons = [
            ("Home", "home"),
            ("Track", "track"),
            ("My Dashboard", "dashboard"),
            ("Logout", "logout")
        ]
        
        for btn_text, page in nav_buttons:
            btn = tk.Button(
                nav_frame,
                text=btn_text,
                font=('Arial', 11),
                bg='#555',
                fg='white',
                activebackground='#777',
                activeforeground='white',
                command=lambda p=page: self.navigate(p),
                padx=20,
                pady=10
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg='#f0f0f0')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show home page by default
        self.navigate("home")
    
    def navigate(self, page):
        """Navigate to different pages"""
        # Clear current page
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if page == "home":
            home_frame = create_home_page(self.content_frame, self.navigate)
            home_frame.pack(fill=tk.BOTH, expand=True)
        
        elif page == "track":
            track_page = TrackPage(self.content_frame, self.navigate)
            track_page.get_frame().pack(fill=tk.BOTH, expand=True)
        
        elif page == "dashboard":
            dashboard_page = DashboardPage(self.content_frame, self.navigate)
            dashboard_page.get_frame().pack(fill=tk.BOTH, expand=True)
        
        elif page == "logout":
            if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
                clear_session()
                self.show_auth_page()
    
    def clear_page(self):
        """Clear current page"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_page_widget = None

def main():
    root = tk.Tk()
    app = FareTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

