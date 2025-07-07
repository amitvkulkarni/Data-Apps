from dash.dependencies import Input, Output, State
from dash import no_update
import folium
import pandas as pd
import os
from llm_handler import get_filters_from_llm


def register_callbacks(app, df_airbnb):
    @app.callback(
        [
            Output("folium-map-llm", "srcDoc"),
            Output("found-locations-output", "children"),
        ],
        [Input("analyze-button", "n_clicks")],
        [State("text-input", "value")],
    )
    def update_map_from_text(n_clicks, text_input):
        if n_clicks == 0 or not text_input:
            # Create and save initial map with all listings
            assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
            initial_map_path = os.path.join(assets_dir, "llm_map_initial.html")

            # Center the map on the average location of all listings
            center_lat = df_airbnb["latitude"].mean()
            center_lon = df_airbnb["longitude"].mean()
            m = folium.Map(
                location=[center_lat, center_lon], zoom_start=11, tiles="OpenStreetMap"
            )

            # Add all listings to the map
            for _, row in df_airbnb.iterrows():
                folium.Marker(
                    location=[row["latitude"], row["longitude"]],
                    popup=f"<b>{row['name']}</b><br>Type: {row['room_type']}<br>Price: ${row['price']}",
                    tooltip=f"Name: {row['name']}<br>Neighbourhood Group: {row['neighbourhood_group']}<br>Neighbourhood: {row['neighbourhood']}<br>Price: ${row['price']}",
                ).add_to(m)

            folium.LayerControl().add_to(m)
            m.save(initial_map_path)

            with open(initial_map_path, "r") as f:
                map_html = f.read()

            return (
                map_html,
                f"Showing all {len(df_airbnb)} listings. Use the search to filter.",
            )

        # --- 1. Get Filters from LLM ---
        llm_filters = get_filters_from_llm(text_input)

        if not llm_filters:
            return no_update, "Could not process your query. Please try again."

        # --- 2. Filter DataFrame ---
        filtered_df = df_airbnb.copy()
        search_criteria = []

        # Define and apply filters in a structured way
        categorical_filters = {
            "neighbourhood_group": "neighbourhood_group",
            "neighbourhood": "neighbourhood",
            "room_type": "room_type",
        }

        for filter_key, df_column in categorical_filters.items():
            if values := llm_filters.get(filter_key):
                if isinstance(values, str):
                    values = [values]

                lower_values = [v.lower() for v in values]

                filtered_df = filtered_df[
                    filtered_df[df_column].str.lower().isin(lower_values)
                ]
                search_criteria.extend(values)

        # Apply numerical filters for price range
        if (price_min := llm_filters.get("price_min")) is not None:
            filtered_df = filtered_df[filtered_df["price"] >= price_min]
            search_criteria.append(f"Min Price: ${price_min}")

        if (price_max := llm_filters.get("price_max")) is not None:
            filtered_df = filtered_df[filtered_df["price"] <= price_max]
            search_criteria.append(f"Max Price: ${price_max}")

        # --- 3. Create Map ---
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        os.makedirs(assets_dir, exist_ok=True)

        if not filtered_df.empty:
            center_lat = filtered_df["latitude"].mean()
            center_lon = filtered_df["longitude"].mean()
            zoom = 12
            output_text = f"Found {len(filtered_df)} listings matching: {', '.join(search_criteria)}"
        else:
            center_lat = 40.730610
            center_lon = -73.935242
            zoom = 10
            output_text = f"No listings found for: {', '.join(search_criteria) if search_criteria else 'your query'}"

        m = folium.Map(
            location=[center_lat, center_lon], zoom_start=zoom, tiles="OpenStreetMap"
        )

        for _, row in filtered_df.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"<b>{row['name']}</b><br>Type: {row['room_type']}<br>Price: ${row['price']}",
                tooltip=f"Name: {row['name']}<br>Neighbourhood Group: {row['neighbourhood_group']}<br>Neighbourhood: {row['neighbourhood']}<br>Room type: {row['room_type']}<br>Price:${row['price']}",
            ).add_to(m)

        folium.LayerControl().add_to(m)
        map_path = os.path.join(assets_dir, "llm_map.html")
        m.save(map_path)

        with open(map_path, "r") as f:
            map_html = f.read()

        return map_html, output_text
