import pandas as pd
import dash
from dash import dcc, html, Output, Input
import plotly.graph_objs as go

# Load air quality data from a CSV file
df = pd.read_csv('AQI and Lat Long of Countries.csv')

# Extract unique countries
countries = sorted(df['Country'].dropna().astype(str).unique())


app = dash.Dash(__name__)

server = app.server

app.title = 'Air Quality Dashboard'



app.layout = html.Div([
    html.H2('Air Quality Dashboard (CSV-based)'),
    
    html.Label('Select a Country:'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in sorted(countries)],
        value=sorted(countries)[0]
    ),

    html.Br(),
    html.Label('Select a City:'),
    dcc.Dropdown(id='city-dropdown'),

    html.Br(),
    html.Div(id='aqi-output'),

    html.Div([
        dcc.Graph(id='pollution-graph', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='map-graph', style={'width': '48%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'space-between'})
], style={'width': '90%', 'margin': 'auto'})

# Callback to update city dropdown based on country
@app.callback(
    Output('city-dropdown', 'options'),
    Output('city-dropdown', 'value'),
    Input('country-dropdown', 'value')
)
def update_cities(selected_country):
    filtered_df = df[df['Country'] == selected_country]
    city_options = [{'label': city, 'value': city} for city in sorted(filtered_df['City'].unique())]
    first_city = city_options[0]['value'] if city_options else None
    return city_options, first_city

# Callback to update visuals based on city selection
@app.callback(
    Output('aqi-output', 'children'),
    Output('pollution-graph', 'figure'),
    Output('map-graph', 'figure'),
    Input('city-dropdown', 'value')
)
def update_air_quality(city):
    city_data = df[df['City'] == city].iloc[0]
    aqi = city_data['AQI Value']
    lat = city_data['lat']
    lon = city_data['lng']
    country = city_data['Country']

    # Pollutant data
    components = city_data.drop(['City', 'AQI Value', 'lat', 'lng', 'Country']).to_dict()
    aqi_text = f"Air Quality Index for {city}, {country}: {aqi}"

    # Horizontal bar chart
    bar_fig = go.Figure(data=[
        go.Bar(
            x=list(components.values()),
            y=list(components.keys()),
            orientation='h',
            marker_color='skyblue'
        )
    ])
    bar_fig.update_layout(title=f'Pollutants in {city}', xaxis_title='Concentration (μg/m³)', yaxis_title='Pollutants')

    # Map figure
    map_fig = go.Figure(go.Scattergeo(
        lon=[lon],
        lat=[lat],
        text=f"{city}, {country}<br>AQI: {aqi}",
        mode='markers',
        marker=dict(size=10, color='red', symbol='circle')
    ))
    map_fig.update_layout(
        title='City Location',
        geo=dict(showland=True, landcolor='lightgrey'),
        height=400
    )

    return aqi_text, bar_fig, map_fig

if __name__ == '__main__':
    app.run(debug=True)
