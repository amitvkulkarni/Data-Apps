import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any

load_dotenv()

# --- 0. Configure Gemini ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
ml_model = RandomForestRegressor(n_estimators=100, random_state=42)
ml_model.fit(X, y)
feature_importances = ml_model.feature_importances_
features = X.columns
importance_df = pd.DataFrame({"Feature": features, "Importance": feature_importances})
importance_df = importance_df.sort_values(by="Importance", ascending=True)


# --- 2. LangGraph Agent ---
class AgentState(TypedDict):
    description: str
    params: Dict[str, Any]
    price: float


def interpret_description_node(state: AgentState):
    prompt = f"""
    Extract the following parameters from the user's description and return them as a JSON object:
    - weather: 0 for sunny, 1 for drizzly, 2 for rainy
    - competitor_price: float
    - inventory_level: float between 0.1 and 1.0
    - time_of_day: int between 0 and 23
    - promotional_event: 0 for no, 1 for yes

    Description: {state['description']}

    Return only the JSON object.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    try:
        json_str = response.text.strip().replace("```json", "").replace("```", "")
        params = json.loads(json_str)
        return {"params": params}
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error decoding LLM response: {e}")
        return {"params": None}


def get_price_prediction_node(state: AgentState):
    if state["params"] is None:
        return {"price": 0.0}
    scenario = pd.DataFrame([state["params"]])
    predicted_price = ml_model.predict(scenario)[0]
    return {"price": predicted_price}


def handle_error_node(state: AgentState):
    print("Error in processing. Please try again.")
    return {"price": 0.0}


def start_node(state: AgentState):
    print("Starting the agent...")
    return state


workflow = StateGraph(AgentState)
workflow.add_node("start", start_node)
workflow.add_node("interpret_description", interpret_description_node)
workflow.add_node("get_price_prediction", get_price_prediction_node)
workflow.add_node("handle_error", handle_error_node)

workflow.set_entry_point("start")
workflow.add_edge("start", "interpret_description")
workflow.add_edge("interpret_description", "get_price_prediction")
workflow.add_edge("get_price_prediction", END)
workflow.add_edge("handle_error", END)

app_agent = workflow.compile()

# --- 3. Dash App Layout ---
app = dash.Dash(__name__)

app.layout = html.Div(
    className="container",
    children=[
        html.H1("Dynamic Pricing with Agentic AI"),
        html.Div(
            className="row",
            style={"display": "flex"},
            children=[
                html.Div(
                    className="control-panel",
                    style={"width": "40%", "padding": "10px"},
                    children=[
                        html.H3("Describe the Pricing Scenario"),
                        dcc.Textarea(
                            id="scenario-input",
                            placeholder="e.g., It is a rainy day, competitor price is $11.50, inventory is low, and it is 3 PM. A promotion is active.",
                            style={"width": "100%", "height": 100},
                        ),
                        html.Button(
                            "Suggest Optimal Price",
                            id="predict-button",
                            className="button",
                        ),
                        dcc.Loading(
                            id="loading-price",
                            type="default",
                            children=html.Div(
                                id="prediction-output",
                                children=[html.H4("Suggested Price:"), html.P("$0.00")],
                            ),
                        ),
                    ],
                ),
                html.Div(
                    className="graph-panel",
                    style={"width": "60%", "padding": "10px"},
                    children=[
                        html.H3("Model Insights"),
                        dcc.Loading(
                            id="loading-graph",
                            type="default",
                            children=dcc.Graph(id="feature-importance-graph"),
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# --- 4. Callbacks ---
@app.callback(
    [
        Output("prediction-output", "children"),
        Output("feature-importance-graph", "figure"),
    ],
    [Input("predict-button", "n_clicks")],
    [State("scenario-input", "value")],
)
def update_prediction_and_graph(n_clicks, description):
    if n_clicks is None or not description:
        return [html.H4("Suggested Price:"), html.P("$0.00")], dash.no_update

    result = app_agent.invoke({"description": description})
    predicted_price = result.get("price", 0.0)

    price_output = [html.H4("Suggested Price:"), html.P(f"${predicted_price:.2f}")]

    fig = {
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

    return price_output, fig


if __name__ == "__main__":
    app.run(debug=True)
