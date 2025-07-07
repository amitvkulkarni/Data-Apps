import dash
from layout import create_layout
from callbacks import register_callbacks
import pandas as pd
import os
import json

# --- 1. App Initialization ---
app = dash.Dash(__name__, assets_folder=os.path.join(os.path.dirname(__file__), '..', 'assets'))

# --- 2. Load Airbnb Data ---
# Load data from the generated JSON file
json_file_path = os.path.join(os.path.dirname(__file__), "..", "dummy_airbnb_data.json")
with open(json_file_path, "r") as f:
    data_airbnb = json.load(f)
df_airbnb = pd.DataFrame(data_airbnb)

# --- 3. App Layout ---
app.layout = create_layout()

# --- 4. Register Callbacks ---
register_callbacks(app, df_airbnb)

# --- 5. Run the App ---
if __name__ == "__main__":
    app.run(debug=False)
