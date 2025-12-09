import tkinter as tk
from tkinter import ttk, messagebox
from fare_calculator import data_entry, load_fare_guide
from database import save_fare_record
from session import load_session

class TrackPage:
    def __init__(self, parent, navigate_callback):
        self.parent = parent
        self.navigate_callback = navigate_callback
        self.frame = tk.Frame(parent, bg='#f0f0f0')
        self.current_route_details = None
        self.current_total = 0.0
        
        # Load fare guide on initialization
        if not load_fare_guide():
            messagebox.showwarning("Warning", "Could not load fare data. Please ensure fare_data.csv exists.")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for the Track page"""
        # Title
        title_label = tk.Label(
            self.frame,
            text="Track Fare",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=20)
        
        # Main container with two boxes side by side
        main_container = tk.Frame(self.frame, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Data Entry Box (left)
        entry_frame = tk.LabelFrame(
            main_container,
            text="Data Entry",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#333',
            padx=15,
            pady=15
        )
        entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # District input
        tk.Label(
            entry_frame,
            text="District (1-6):",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))
        self.district_entry = tk.Entry(entry_frame, font=('Arial', 10))
        self.district_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Start location input
        tk.Label(
            entry_frame,
            text="Start Location:",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))
        self.start_entry = tk.Entry(entry_frame, font=('Arial', 10))
        self.start_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Destination input
        tk.Label(
            entry_frame,
            text="Destination:",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))
        self.destination_entry = tk.Entry(entry_frame, font=('Arial', 10))
        self.destination_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Include trike input
        tk.Label(
            entry_frame,
            text="Include Trike (y/n):",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))
        self.trike_entry = tk.Entry(entry_frame, font=('Arial', 10))
        self.trike_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Calculate button
        calculate_btn = tk.Button(
            entry_frame,
            text="Calculate Fare",
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            command=self.calculate_fare,
            padx=20,
            pady=10
        )
        calculate_btn.pack(pady=10)
        
        # Fare Display Box (right)
        display_frame = tk.LabelFrame(
            main_container,
            text="Fare Display",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#333',
            padx=15,
            pady=15
        )
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Route details display
        tk.Label(
            display_frame,
            text="Route Details:",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))
        
        # Text widget with scrollbar for route details
        text_frame = tk.Frame(display_frame, bg='#ffffff')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.route_text = tk.Text(
            text_frame,
            font=('Arial', 9),
            bg='#f9f9f9',
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED
        )
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.route_text.yview)
        self.route_text.configure(yscrollcommand=scrollbar.set)
        
        self.route_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Total fare display
        self.total_label = tk.Label(
            display_frame,
            text="Total Fare: ₱0.00",
            font=('Arial', 14, 'bold'),
            bg='#ffffff',
            fg='#0066cc'
        )
        self.total_label.pack(pady=10)
        
        # Save button
        self.save_btn = tk.Button(
            display_frame,
            text="Save Record",
            font=('Arial', 11, 'bold'),
            bg='#2196F3',
            fg='white',
            command=self.save_record,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.save_btn.pack(pady=10)
        
        # Success message label
        self.success_label = tk.Label(
            display_frame,
            text="",
            font=('Arial', 10),
            bg='#ffffff',
            fg='#4CAF50'
        )
        self.success_label.pack()
    
    def calculate_fare(self):
        """Calculate fare based on user input"""
        # Reload fare guide to ensure it's up to date
        if not load_fare_guide():
            messagebox.showerror("Error", "Fare data not loaded. Please ensure fare_data.csv exists.")
            return
        
        district = self.district_entry.get().strip()
        start_location = self.start_entry.get().strip()
        destination = self.destination_entry.get().strip()
        include_trike = self.trike_entry.get().strip()
        
        # Validate inputs
        if not all([district, start_location, destination, include_trike]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Process data entry
        total_fare, route_details, error = data_entry(district, start_location, destination, include_trike)
        
        if error:
            messagebox.showerror("Error", error)
            return
        
        if total_fare is None:
            messagebox.showerror("Error", "Could not calculate fare")
            return
        
        # Store for saving
        self.current_total = total_fare
        self.current_route_details = route_details
        self.current_district = district
        self.current_start = start_location
        self.current_destination = destination
        self.current_trike = include_trike
        
        # Display route details
        self.route_text.config(state=tk.NORMAL)
        self.route_text.delete(1.0, tk.END)
        
        route_text = "Calculated Route:\n\n"
        for detail in route_details:
            route_text += f"{detail['segment']} ({detail['transport_type']}): ₱{detail['fare']:.2f}\n"
        
        self.route_text.insert(1.0, route_text)
        self.route_text.config(state=tk.DISABLED)
        
        # Update total fare
        self.total_label.config(text=f"Total Fare: ₱{total_fare:.2f}")
        
        # Enable save button
        self.save_btn.config(state=tk.NORMAL)
        
        # Clear success message
        self.success_label.config(text="")
    
    def save_record(self):
        """Save fare record to database"""
        srcode = load_session()
        if not srcode:
            messagebox.showerror("Error", "Please login first")
            self.navigate_callback("logout")
            return
        
        # Convert district to int for database
        try:
            district_int = int(self.current_district)
        except ValueError:
            messagebox.showerror("Error", "Invalid district value")
            return
        
        if save_fare_record(
            srcode,
            district_int,
            self.current_start,
            self.current_destination,
            self.current_trike,
            self.current_total
        ):
            self.success_label.config(text="Data saved successfully!")
            messagebox.showinfo("Success", "Data saved successfully!")
            
            # Clear inputs
            self.district_entry.delete(0, tk.END)
            self.start_entry.delete(0, tk.END)
            self.destination_entry.delete(0, tk.END)
            self.trike_entry.delete(0, tk.END)
            
            # Clear display
            self.route_text.config(state=tk.NORMAL)
            self.route_text.delete(1.0, tk.END)
            self.route_text.config(state=tk.DISABLED)
            self.total_label.config(text="Total Fare: ₱0.00")
            self.save_btn.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Failed to save record")
    
    def get_frame(self):
        """Return the frame widget"""
        return self.frame

