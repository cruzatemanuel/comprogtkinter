import tkinter as tk
from tkinter import ttk, messagebox
from database import get_user, get_user_fares, delete_fare_record, update_college, get_weekly_average
from session import load_session

class DashboardPage:
    def __init__(self, parent, navigate_callback):
        self.parent = parent
        self.navigate_callback = navigate_callback
        self.frame = tk.Frame(parent, bg='#f0f0f0')
        self.user_data = None
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create all widgets for the Dashboard page"""
        # Title
        title_label = tk.Label(
            self.frame,
            text="My Dashboard",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=20)
        
        # Side-by-side boxes container
        boxes_container = tk.Frame(self.frame, bg='#f0f0f0')
        boxes_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # User Info Box (left)
        self.user_info_frame = tk.LabelFrame(
            boxes_container,
            text="User Information",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#333',
            padx=15,
            pady=15
        )
        self.user_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # User info labels (will be populated)
        self.srcode_label = tk.Label(
            self.user_info_frame,
            text="SRCODE: -",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        )
        self.srcode_label.pack(fill=tk.X, pady=5)
        
        self.name_label = tk.Label(
            self.user_info_frame,
            text="Name: -",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        )
        self.name_label.pack(fill=tk.X, pady=5)
        
        # College section with update functionality
        college_label_frame = tk.Frame(self.user_info_frame, bg='#ffffff')
        college_label_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            college_label_frame,
            text="College:",
            font=('Arial', 10),
            bg='#ffffff',
            anchor='w'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.college_label = tk.Label(
            college_label_frame,
            text="-",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            anchor='w',
            fg='#0066cc'
        )
        self.college_label.pack(side=tk.LEFT, padx=5)
        
        # College update section
        update_frame = tk.Frame(self.user_info_frame, bg='#ffffff')
        update_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            update_frame,
            text="Update College:",
            font=('Arial', 9),
            bg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, pady=(5, 0))
        
        self.college_entry = tk.Entry(update_frame, font=('Arial', 10))
        self.college_entry.pack(fill=tk.X, pady=5)
        
        update_btn = tk.Button(
            update_frame,
            text="Update",
            font=('Arial', 10),
            bg='#4CAF50',
            fg='white',
            command=self.update_college,
            padx=15,
            pady=5
        )
        update_btn.pack(pady=5)
        
        # Weekly Average Box (right)
        self.weekly_avg_frame = tk.LabelFrame(
            boxes_container,
            text="Weekly Average",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#333',
            padx=15,
            pady=15
        )
        self.weekly_avg_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.avg_label = tk.Label(
            self.weekly_avg_frame,
            text="Average Fare (Last 7 Days):\n₱0.00",
            font=('Arial', 14, 'bold'),
            bg='#ffffff',
            fg='#0066cc',
            justify=tk.CENTER
        )
        self.avg_label.pack(expand=True)
        
        # History Section
        history_frame = tk.LabelFrame(
            self.frame,
            text="Fare History",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#333',
            padx=15,
            pady=15
        )
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            history_frame,
            text="Refresh",
            font=('Arial', 10),
            bg='#2196F3',
            fg='white',
            command=self.load_data,
            padx=15,
            pady=5
        )
        refresh_btn.pack(anchor=tk.E, pady=(0, 10))
        
        # Treeview for history table
        columns = ('Date', 'District', 'Start', 'Destination', 'Trike', 'Total Fare', 'ID')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=10)
        
        # Configure column headings
        self.history_tree.heading('Date', text='Date')
        self.history_tree.heading('District', text='District')
        self.history_tree.heading('Start', text='Start Location')
        self.history_tree.heading('Destination', text='Destination')
        self.history_tree.heading('Trike', text='Trike')
        self.history_tree.heading('Total Fare', text='Total Fare')
        self.history_tree.heading('ID', text='ID')
        
        # Configure column widths
        self.history_tree.column('Date', width=150)
        self.history_tree.column('District', width=80)
        self.history_tree.column('Start', width=150)
        self.history_tree.column('Destination', width=150)
        self.history_tree.column('Trike', width=60)
        self.history_tree.column('Total Fare', width=100)
        self.history_tree.column('ID', width=50)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button
        delete_btn = tk.Button(
            history_frame,
            text="Delete Selected Record",
            font=('Arial', 10, 'bold'),
            bg='#f44336',
            fg='white',
            command=self.delete_record,
            padx=15,
            pady=10
        )
        delete_btn.pack(pady=10)
    
    def load_data(self):
        """Load user data and fare history"""
        srcode = load_session()
        if not srcode:
            messagebox.showerror("Error", "Please login first")
            self.navigate_callback("logout")
            return
        
        # Load user data
        self.user_data = get_user(srcode)
        if self.user_data:
            self.srcode_label.config(text=f"SRCODE: {self.user_data.get('srcode', '-')}")
            self.name_label.config(text=f"Name: {self.user_data.get('name', '-')}")
            self.college_label.config(text=self.user_data.get('college', '-'))
        else:
            messagebox.showerror("Error", "Could not load user data")
            return
        
        # Load weekly average
        avg_fare = get_weekly_average(srcode)
        self.avg_label.config(text=f"Average Fare (Last 7 Days):\n₱{avg_fare:.2f}")
        
        # Load fare history
        self.load_history()
    
    def load_history(self):
        """Load fare history into treeview"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        srcode = load_session()
        if not srcode:
            return
        
        fares = get_user_fares(srcode)
        for fare in fares:
            # Format date
            try:
                if fare.get('created_date'):
                    if hasattr(fare['created_date'], 'strftime'):
                        date_str = fare['created_date'].strftime('%Y-%m-%d %H:%M')
                    else:
                        date_str = str(fare['created_date'])
                else:
                    date_str = '-'
            except Exception:
                date_str = '-'
            
            self.history_tree.insert('', tk.END, values=(
                date_str,
                fare.get('district', '-'),
                fare.get('start_location', '-'),
                fare.get('destination', '-'),
                fare.get('include_trike', '-'),
                f"₱{fare.get('total_fare', 0.0):.2f}",
                fare.get('id', '-')
            ))
    
    def update_college(self):
        """Update user's college"""
        new_college = self.college_entry.get().strip()
        if not new_college:
            messagebox.showerror("Error", "Please enter a college name")
            return
        
        srcode = load_session()
        if not srcode:
            messagebox.showerror("Error", "Please login first")
            self.navigate_callback("logout")
            return
        
        if update_college(srcode, new_college):
            messagebox.showinfo("Success", "College updated successfully!")
            self.college_entry.delete(0, tk.END)
            self.load_data()  # Refresh data
        else:
            messagebox.showerror("Error", "Failed to update college")
    
    def delete_record(self):
        """Delete selected fare record"""
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        # Get record ID from selected item
        item = self.history_tree.item(selected[0])
        record_id = item['values'][6]  # ID is in the last column
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            if delete_fare_record(record_id):
                messagebox.showinfo("Success", "Record deleted successfully!")
                self.load_history()  # Refresh history
            else:
                messagebox.showerror("Error", "Failed to delete record")
    
    def get_frame(self):
        """Return the frame widget"""
        return self.frame

