import os
import pandas as pd
import openai
from datetime import datetime
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Set up OpenAI API credentials
# Create .env file and insert your api key like so:
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
# openai.api_key = os.getenv("OPENAI_API_KEY")   # pip install python-dotenv
openai.api_key = OPENAI_API_KEY
# Initialize the ChatGPT model
model_engine = "text-davinci-003"

# Instantiate the Dash app
app = Dash(__name__)

answer_list = []
df = pd.DataFrame()

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "CHAT WITH GENERATIVE AI",
                            style={
                                "text-align": "center",
                                "font-size": 30,
                                "font-weight": "bold",
                                "color": "#2E86C1",
                            },
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dcc.Textarea(
                    id="input-text",
                    style={"width": "50%", "height": 75, "margin-left": "350px"},
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Button(
                    "SEND",
                    id="submit-button",
                    n_clicks=0,
                    style={
                        "backgroundColor": "blue",
                        "font-size": 12,
                        "font-weight": "bold",
                        "color": "white",
                        "margin-left": "350px",
                    },
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dcc.Loading(
                    [
                        html.Div(
                            id="output-text",
                            style={
                                "margin-left": "350px",
                                "font-size": 17,
                                "font-weight": "bold",
                                "color": "Teal",
                                "width": "50%",
                            },
                        )
                    ],
                    type="default",
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Div(
            id="output-chat-history",
            style={
                "text-align": "left",
                "margin-left": "350px",
                "font-size": 12,
                "font-weight": "bold",
                "color": "#2E86C1",
            },
        ),
        html.Div(
            id="output-text-track",
            style={
                "whiteSpace": "pre-line",
                "margin-left": "350px",
                "width": "50%",
                "margin-top": "10px",
            },
        ),
    ]
)


# Define the callback function
@app.callback(
    [
        Output("output-text", "children"),
        Output("output-text-track", "children"),
        Output("output-chat-history", "children"),
    ],
    Input("submit-button", "n_clicks"),
    State("input-text", "value"),
)
def update_output(n_clicks, input_text):
    if n_clicks > 0:
        # Get the response from ChatGPT
        response = openai.Completion.create(
            engine=model_engine,
            prompt=f"{input_text}\n",
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        generated_text = response.choices[0].text
        answer_list_time = f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {input_text}\n{generated_text}\n'
        answer_list.insert(0, answer_list_time)

        return (
            generated_text,
            answer_list,
            f"RECENT CHAT HISTORY ( {len(answer_list)} )",
        )

    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
