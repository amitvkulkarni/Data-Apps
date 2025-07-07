
import pandas as pd
import random
import json
import os

# Define possible values for dummy data
NEIGHBOURHOOD_GROUPS = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
NEIGHBOURHOODS = {
    'Manhattan': ['Midtown', 'Financial District', 'Chelsea', 'Upper East Side', 'Harlem'],
    'Brooklyn': ['Williamsburg', 'Bushwick', 'Greenpoint', 'Park Slope', 'DUMBO'],
    'Queens': ['Astoria', 'Long Island City', 'Flushing', 'Jackson Heights', 'Forest Hills'],
    'Bronx': ['Mott Haven', 'Riverdale', 'Fordham', 'Pelham Bay'],
    'Staten Island': ['St. George', 'Tottenville', 'New Dorp']
}
ROOM_TYPES = ['Entire home/apt', 'Private room', 'Shared room']

def generate_dummy_airbnb_data(num_records=50):
    data = []
    for i in range(1, num_records + 1):
        group = random.choice(NEIGHBOURHOOD_GROUPS)
        hood = random.choice(NEIGHBOURHOODS[group])
        
        # Generate realistic-ish coordinates for NYC
        # Base coordinates for NYC: ~40.7128° N, 74.0060° W
        # Add small random offsets
        latitude = 40.7 + (random.random() - 0.5) * 0.2 # +/- 0.1 degree
        longitude = -74.0 + (random.random() - 0.5) * 0.2 # +/- 0.1 degree

        data.append({
            'id': i,
            'name': f'{random.choice(["Cozy", "Spacious", "Charming", "Luxury", "Quiet", "Modern", "Sunny", "Artist"])} {random.choice(["Studio", "Loft", "Room", "Apt", "Getaway", "Home", "Flat"])} in {hood}',
            'neighbourhood_group': group,
            'neighbourhood': hood,
            'latitude': round(latitude, 6),
            'longitude': round(longitude, 6),
            'room_type': random.choice(ROOM_TYPES),
            'price': random.randint(50, 500)
        })
    return data

if __name__ == "__main__":
    dummy_data = generate_dummy_airbnb_data(50)
    
    # Define the path to save the JSON file
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'dummy_airbnb_data.json')
    
    with open(json_file_path, 'w') as f:
        json.dump(dummy_data, f, indent=4)
    
    print(f"Generated {len(dummy_data)} records and saved to {json_file_path}")
