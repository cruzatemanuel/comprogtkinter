# Fare Tracker Application

A tkinter desktop application for tracking and calculating transportation fares in Batangas, with MySQL database backend.

## Features

- **User Authentication**: Sign up and login with SRCODE
- **Fare Calculation**: Calculate transportation fares based on routes across 6 districts
- **Fare History**: Track and view all your fare calculations
- **Dashboard**: View user profile, weekly averages, and manage fare records
- **CRUD Operations**: Full Create, Read, Update, Delete functionality

## Requirements

- Python 3.7 or higher
- MySQL Server
- tkinter (usually included with Python)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup MySQL Database:**
   - Make sure MySQL server is running
   - **Create the database and tables manually:**
     ```sql
     CREATE DATABASE faretracker_db;
     
     USE faretracker_db;
     
     CREATE TABLE users (
         srcode VARCHAR(50) PRIMARY KEY,
         name VARCHAR(100) NOT NULL,
         password VARCHAR(100) NOT NULL,
         college VARCHAR(100) NOT NULL
     );
     
     CREATE TABLE fare_history (
         id INT AUTO_INCREMENT PRIMARY KEY,
         srcode VARCHAR(50) NOT NULL,
         district INT NOT NULL,
         start_location VARCHAR(100) NOT NULL,
         destination VARCHAR(100) NOT NULL,
         include_trike VARCHAR(1) NOT NULL,
         total_fare DECIMAL(10, 2) NOT NULL,
         created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
         FOREIGN KEY (srcode) REFERENCES users(srcode) ON DELETE CASCADE
     );
     ```
   - Default connection settings:
     - Host: localhost
     - Port: 3306
     - User: root
     - Password: (empty)
     - Database: faretracker_db

3. **Prepare Fare Data CSV:**
   - Create a file named `fare_data.csv` in the project root
   - The CSV should contain fare route data in the format:
     ```
     route_name,segment,transport_type,fare
     Balayan - BSU,Balayan to Grand Terminal,bus,106.00
     Balayan - BSU,Grand Terminal to BSU,jeepney,13.00
     ...
     ```

## Database Configuration

To change database connection settings, edit `database.py` and modify the `DB_CONFIG` dictionary:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'faretracker_db'
}
```

## Running the Application

```bash
python main.py
```

## Application Structure

- `main.py` - Main application entry point
- `database.py` - MySQL database operations
- `auth.py` - Authentication functions
- `session.py` - Session management
- `fare_calculator.py` - Fare calculation logic
- `ui_home.py` - Home page UI
- `ui_track.py` - Track page UI
- `ui_dashboard.py` - Dashboard page UI

## Usage

1. **Sign Up**: Create a new account with SRCODE, Name, Password, and College
2. **Login**: Use your SRCODE and password to login
3. **Track Fare**: 
   - Enter district (1-6)
   - Enter start location and destination
   - Specify if trike is included (y/n)
   - Click "Calculate Fare" to see the route and total
   - Click "Save Record" to save the calculation
4. **My Dashboard**: 
   - View your profile information
   - Update your college
   - View weekly average fare
   - View and delete fare history records

## Notes

- Passwords are stored in plain text (as specified)
- SRCODE is stored in `session.txt` file for session management
- All location inputs are converted to lowercase
- Database and tables must be created manually before running the application

## Troubleshooting

- **Database Connection Error**: Make sure MySQL server is running and connection settings are correct
- **CSV File Not Found**: Ensure `fare_data.csv` exists in the project root directory
- **Import Errors**: Make sure all dependencies are installed using `pip install -r requirements.txt`

