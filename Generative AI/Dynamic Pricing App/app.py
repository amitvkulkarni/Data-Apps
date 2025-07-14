import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# --- 1. Model Training (Runs once at startup) ---
num_samples = 1000
np.random.seed(42)
weather_conditions = np.random.randint(0, 3, num_samples)
competitor_price = np.random.normal(loc=10.0, scale=1.0, size=num_samples)
inventory_level = np.random.uniform(low=0.1, high=1.0, size=num_samples)
time_of_day = np.random.randint(0, 24, num_samples)
promotional_event = np.random.randint(0, 2, num_samples)
base_price = 10.0
our_price = (
    base_price
    + (weather_conditions * 0.5)
    + (1 - inventory_level) * 2.0
    + (competitor_price - base_price) * 0.8
    + (time_of_day / 24 * 1.0)
    + (promotional_event * -1.5)
    + np.random.normal(loc=0, scale=0.5, size=num_samples)
)
our_price = np.maximum(our_price, 7.0)
data = pd.DataFrame(
    {
        "weather": weather_conditions,
        "competitor_price": competitor_price,
        "inventory_level": inventory_level,
        "time_of_day": time_of_day,
        "promotional_event": promotional_event,
        "our_price": our_price,
    }
)
X = data[
    [
        "weather",
        "competitor_price",
        "inventory_level",
        "time_of_day",
        "promotional_event",
    ]
]
y = data["our_price"]
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)
feature_importances = model.feature_importances_
features = X.columns
importance_df = pd.DataFrame({"Feature": features, "Importance": feature_importances})
importance_df = importance_df.sort_values(by="Importance", ascending=True)

# --- 2. Dash App Layout ---
app = dash.Dash(__name__)

app.layout = html.Div(
    className="container",
    children=[
        html.H1("Dynamic Pricing & Visualization Dashboard"),
        html.Div(
            className="row",
            style={"display": "flex"},
            children=[
                html.Div(
                    className="control-panel",
                    style={"width": "40%", "padding": "10px"},
                    children=[
                        html.H3("Pricing Scenario"),
                        html.Div(
                            className="input-group",
                            children=[
                                html.Label("Weather Condition"),
                                dcc.Dropdown(
                                    id="weather-input",
                                    options=[
                                        {"label": "☀️ Sunny", "value": 0},
                                        {"label": "🌦️ Drizzly", "value": 1},
                                        {"label": "🌧️ Rainy", "value": 2},
                                    ],
                                    value=0,
                                ),
                            ],
                        ),
                        html.Div(
                            className="input-group",
                            children=[
                                html.Label("Competitor's Price ($)"),
                                dcc.Input(
                                    id="competitor-price-input",
                                    type="number",
                                    value=10.0,
                                    step=0.1,
                                ),
                            ],
                        ),
                        html.Div(
                            className="input-group",
                            children=[
                                html.Label("Inventory Level"),
                                dcc.Slider(
                                    id="inventory-level-input",
                                    min=0.1,
                                    max=1.0,
                                    step=0.05,
                                    value=0.5,
                                    marks={i / 10: str(i / 10) for i in range(1, 11)},
                                ),
                            ],
                        ),
                        html.Div(
                            className="input-group",
                            children=[
                                html.Label("Time of Day (0-23h)"),
                                dcc.Slider(
                                    id="time-of-day-input",
                                    min=0,
                                    max=23,
                                    step=1,
                                    value=12,
                                    marks={i: str(i) for i in range(0, 24, 3)},
                                ),
                            ],
                        ),
                        html.Div(
                            className="input-group",
                            children=[
                                html.Label("Promotional Event"),
                                dcc.Dropdown(
                                    id="promo-input",
                                    options=[
                                        {"label": "No Promotion", "value": 0},
                                        {"label": "Active Promotion", "value": 1},
                                    ],
                                    value=0,
                                ),
                            ],
                        ),
                        html.Button(
                            "Suggest Optimal Price",
                            id="predict-button",
                            className="button",
                        ),
                        html.Div(
                            id="prediction-output",
                            children=[html.H4("Suggested Price:"), html.P("$0.00")],
                        ),
                    ],
                ),
                html.Div(
                    className="graph-panel",
                    style={"width": "60%", "padding": "10px"},
                    children=[
                        html.H3("Model Insights"),
                        dcc.Graph(id="feature-importance-graph"),
                    ],
                ),
            ],
        ),
    ],
)


# --- 3. Callbacks ---
@app.callback(
    Output("prediction-output", "children"),
    [Input("predict-button", "n_clicks")],
    [
        State("weather-input", "value"),
        State("competitor-price-input", "value"),
        State("inventory-level-input", "value"),
        State("time-of-day-input", "value"),
        State("promo-input", "value"),
    ],
)
def update_prediction(n_clicks, weather, competitor_price, inventory, time, promo):
    if n_clicks is None:
        return [html.H4("Suggested Price:"), html.P("$0.00")]

    scenario = pd.DataFrame(
        {
            "weather": [weather],
            "competitor_price": [competitor_price],
            "inventory_level": [inventory],
            "time_of_day": [time],
            "promotional_event": [promo],
        }
    )
    predicted_price = model.predict(scenario)[0]
    price_output = [html.H4("Suggested Price:"), html.P(f"${predicted_price:.2f}")]

    return price_output


@app.callback(
    Output("feature-importance-graph", "figure"), [Input("predict-button", "n_clicks")]
)
def update_graph(n_clicks):
    if n_clicks is None:
        return dash.no_update
    return {
        "data": [
            go.Bar(
                y=importance_df["Feature"],
                x=importance_df["Importance"],
                orientation="h",
                marker={"color": "#007BFF"},
            )
        ],
        "layout": go.Layout(
            title="Feature Importance (What Drives Price)",
            xaxis={"title": "Importance Score"},
            yaxis={"title": "Feature"},
            plot_bgcolor="#fff",
            paper_bgcolor="#fff",
            font={"color": "#333"},
            margin={"l": 150},
        ),
    }


if __name__ == "__main__":
    app.run(debug=True)
