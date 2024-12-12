import openai
import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from typing import List, Dict


# Define the LLMWrapper class
class LLMWrapper:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        openai.api_key = api_key

    def _preprocess_input(self, user_input: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]

    def _postprocess_output(self, response: dict[str, str]) -> str:
        return response.choices[0].message.content.strip()

    def query(self, user_input: str) -> str:
        preprocessed_input = self._preprocess_input(user_input)
        try:
            response = openai.chat.completions.create(
                model=self.model_name, messages=preprocessed_input, max_tokens=100
            )
            return self._postprocess_output(response)
        except Exception as e:
            return f"Error occurred: {str(e)}"


# Initialize the Dash app
app = dash.Dash(__name__)

# Instantiate LLMWrapper
llm_wrapper = LLMWrapper(
    model_name="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY")
)

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("LLM Query Interface", style={"textAlign": "center"}),
        # User input text box
        dcc.Input(
            id="user-input",
            type="text",
            placeholder="Enter your query here...",
            style={"width": "80%", "padding": "10px"},
        ),
        # Submit button
        html.Button(
            "Submit",
            id="submit-btn",
            n_clicks=0,
            style={"padding": "10px", "margin": "10px"},
        ),
        # Display the response from the LLM
        html.Div(
            id="output-response",
            style={"padding": "10px", "marginTop": "20px", "fontSize": "18px"},
        ),
    ]
)


# Define callback to update output based on user input
@app.callback(
    Output("output-response", "children"),
    [Input("submit-btn", "n_clicks")],
    [dash.dependencies.State("user-input", "value")],
)
def update_output(n_clicks, user_input):
    if n_clicks > 0 and user_input:
        # Get the LLM response
        llm_response = llm_wrapper.query(user_input)
        return llm_response
    return ""


# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
