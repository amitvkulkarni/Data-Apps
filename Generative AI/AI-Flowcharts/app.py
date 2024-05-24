import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import base64
import os
import google.generativeai as genai
import requests

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Description your workflow:"),
                        dcc.Textarea(
                            id="description-input",
                            style={"width": "100%", "height": 150},
                        ),
                        dbc.Button(
                            "Submit",
                            id="submit-button",
                            color="primary",
                            className="mt-3",
                        ),
                        dcc.Loading(
                            id="loading-spinner",
                            type="default",
                            children=[
                                html.Div(id="loading-output", style={"display": "none"})
                            ],
                        ),
                    ],
                    width=12,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Generated Flowchart"),
                        html.Img(
                            id="flowchart-image",
                            style={"width": "50%"},
                            width="auto",
                            height="auto",
                        ),
                    ],
                    width=12,
                ),
            ]
        ),
    ],
    fluid=True,
)


def get_gemini_response(input):
    """
    Generate flowchart DOT code based on the user input.

    Parameters:
    input (str): Description of the workflow.

    Returns:
    str: Generated flowchart DOT code.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        print(f"Error generating flowchart: {e}")
        return None


def get_image_graphviz(dot_code):
    """
    Convert flowchart DOT code to PNG image.

    Parameters:
    dot_code (str): Flowchart DOT code.

    Returns:
    str: Base64-encoded PNG image.
    """
    try:
        # Remove triple backticks and 'dot' text
        formatted_out = dot_code.strip("```dot")
        # Remove leading and trailing whitespace
        formatted_out = formatted_out.strip()

        # Find the line containing the rankdir attribute
        lines = formatted_out.split("\n")
        for i, line in enumerate(lines):
            if "rankdir" in line:
                # Modify the rankdir attribute to display the workflow vertically
                lines[i] = "    rankdir=TB;"

        # Reconstruct the DOT code with the modified rankdir attribute
        formatted_out = "\n".join(lines)

        quickchart_url = "https://quickchart.io/graphviz"

        dot_code = formatted_out
        # Prepare the payload for QuickChart
        post_data = {
            "graph": dot_code,
            "format": "png",
        }  # Specify that we want a PNG image

        # Send the POST request to QuickChart API
        response = requests.post(quickchart_url, json=post_data, verify=False)
        response.raise_for_status()

        # Check if the response content is PNG
        content_type = response.headers.get("content-type", "").lower()
        if "image/png" in content_type:
            # Save PNG content to a file
            png_content = response.content
            with open("flowchart.png", "wb") as f:
                f.write(png_content)
            print("Flowchart saved as flowchart.png")

            # Encode PNG content to base64
            encoded_image = base64.b64encode(png_content).decode("ascii")
            return f"data:image/png;base64,{encoded_image}"
        else:
            print("Unexpected response content type:", content_type)
            return None
    except Exception as e:
        print(f"Error converting DOT code to PNG: {e}")
        return None


# Define callback function to update flowchart image
@app.callback(
    [Output("flowchart-image", "src"), Output("loading-output", "children")],
    Input("submit-button", "n_clicks"),
    State("description-input", "value"),
)
def update_flowchart(n_clicks, description):
    """
    Update the flowchart image when the Submit button is clicked.

    Parameters:
    n_clicks (int): Number of times the Submit button has been clicked.
    description (str): Description of the workflow.

    Returns:
    str: Base64-encoded PNG image.
    str: Empty string.
    """
    if n_clicks is None or description is None:
        return dash.no_update, dash.no_update

    # Generate flowchart DOT code based on user input
    description += ". Please use Graphviz DOT Language. Try to make it as detailed as possible with all the steps involved in the process."

    dot_code = get_gemini_response(description)

    if dot_code is None:
        return dash.no_update, "Error generating flowchart"

    # Convert DOT code to PNG image and get base64-encoded string
    encoded_image = get_image_graphviz(dot_code)

    if encoded_image is None:
        return dash.no_update, "Error converting DOT code to PNG"

    return encoded_image, ""


if __name__ == "__main__":
    app.run_server(debug=True)
