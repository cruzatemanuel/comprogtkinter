import csv
import os

# Global variable to store fare guide data
fare_guide = {}

def load_fare_guide():
    """Load fare data from CSV file"""
    global fare_guide
    fare_guide = {}
    
    csv_file = "fare_data.csv"
    if not os.path.exists(csv_file):
        print(f"Warning: {csv_file} not found")
        return False
    
    try:
        current_route = None
        current_district = None
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this is a district line (e.g., "district 1:")
                if line.lower().startswith('district'):
                    # Extract district number if needed
                    current_district = line
                    continue
                
                # Check if this is a route header (contains " - " and ends with ":")
                # Format: "Balayan - BSU:" or "BSU - Balayan:"
                if " - " in line and line.endswith(':'):
                    # Remove colon and convert to lowercase for matching
                    current_route = line.rstrip(':').strip().lower()
                    fare_guide[current_route] = []
                elif current_route:
                    # This is a segment line: "segment,transport_type,fare"
                    # Format: "Balayan to Grand Terminal,bus,106.00"
                    parts = line.split(',')
                    if len(parts) >= 3:
                        segment = parts[0].strip()
                        transport_type = parts[1].strip()
                        try:
                            fare = float(parts[2].strip())
                            fare_guide[current_route].append({
                                'segment': segment,
                                'transport_type': transport_type,
                                'fare': fare
                            })
                        except ValueError:
                            continue  # Skip invalid fare values
                    elif len(parts) == 1 and " - " in line:
                        # This might be a new route header without colon, reset current_route
                        # But in the provided format, all route headers have colons
                        pass
        
        print(f"Loaded {len(fare_guide)} routes from CSV")
        return True
    except Exception as e:
        print(f"Error loading fare guide: {e}")
        import traceback
        traceback.print_exc()
        return False

def is_valid_location(location):
    """Check if location exists in fare guide"""
    location_lower = location.lower()
    for route in fare_guide.keys():
        # Check if location is part of any route
        if location_lower in route:
            return True
    return False

def find_record(start_location, destination):
    """Find route record matching start and destination"""
    if not fare_guide:
        return None
    
    start_lower = start_location.lower().strip()
    dest_lower = destination.lower().strip()
    
    # Try direct route: "start - destination"
    route_key1 = f"{start_lower} - {dest_lower}"
    if route_key1 in fare_guide:
        return fare_guide[route_key1]
    
    # Try reverse route: "destination - start"
    route_key2 = f"{dest_lower} - {start_lower}"
    if route_key2 in fare_guide:
        return fare_guide[route_key2]
    
    return None

def calculate_fare(start_location, destination, include_trike):
    """Calculate total fare for a route"""
    segments = find_record(start_location, destination)
    
    if not segments:
        return None, "Route not found"
    
    total = 0.0
    route_details = []
    
    for segment in segments:
        fare = segment['fare']
        total += fare
        route_details.append({
            'segment': segment['segment'],
            'transport_type': segment['transport_type'],
            'fare': fare
        })
    
    # Add trike fee if applicable
    if include_trike and include_trike.lower().strip() == 'y':
        total += 20.00
        route_details.append({
            'segment': 'Trike fee',
            'transport_type': 'trike',
            'fare': 20.00
        })
    
    return total, route_details

def data_entry(district, start_location, destination, include_trike):
    """Main function to process fare calculation input"""
    # Validate inputs are not empty
    if not start_location or not destination:
        return None, None, "Start location and destination are required"
    
    # Convert inputs to lowercase
    start_location = start_location.lower().strip()
    destination = destination.lower().strip()
    
    if not start_location or not destination:
        return None, None, "Start location and destination cannot be empty"
    
    include_trike = include_trike.lower().strip() if include_trike else 'n'
    
    # Validate district
    try:
        district_num = int(district)
        if district_num < 1 or district_num > 6:
            return None, None, "District must be between 1 and 6"
    except (ValueError, TypeError):
        return None, None, "District must be a number between 1 and 6"
    
    # Validate trike option
    if include_trike not in ['y', 'n']:
        return None, None, "Include trike must be 'y' or 'n'"
    
    # Calculate fare
    total_fare, route_details = calculate_fare(start_location, destination, include_trike)
    
    if total_fare is None:
        return None, None, route_details  # route_details contains error message
    
    return total_fare, route_details, None

