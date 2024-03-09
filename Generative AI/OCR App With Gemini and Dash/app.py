import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import base64
from datetime import datetime
from PIL import Image
import io
import os
import google.generativeai as genai


# Fetch the API key from the environment variable
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


response_list = []

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Gemini Image Demo"

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define style for the gray border
section_style = {
    "border": "1px solid #dddddd",
    "border-radius": "5px",
    "padding": "10px",
    "margin": "10px auto",
    "width": "50%",
    "textAlign": "center",
}

# Define style for the button without border
button_style = {
    "background-color": "#2E86C1",
    "color": "white",
}

app.layout = html.Div(
    [
        html.H1(
            "MULTI-LANGUAGE OCR USING GEMINI & DASH",
            style={
                "textAlign": "center",
                "color": "#2E86C1",
                "fontSize": "25px",
                "fontWeight": "bold",
            },
        ),
        html.Div(
            [
                html.H2(
                    "UPLOAD IMAGE",
                    style={
                        "color": "#F08080",
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "textAlign": "left",
                    },
                ),
                dcc.Upload(
                    id="upload-image",
                    children=html.Div(["Drag and Drop or ", html.A("Select an Image")]),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "color": "#333333",
                    },
                    # Allow multiple files to be uploaded
                    multiple=False,
                ),
            ],
            style=section_style,
        ),
        html.Div(
            [
                html.H2(
                    "INPUT PROMPT",
                    style={
                        "color": "#F08080",
                        "textAlign": "left",
                        "fontSize": "18px",
                        "fontWeight": "bold",
                    },
                ),
                dcc.Input(
                    id="input",
                    type="text",
                    placeholder="Enter Input Prompt",
                    style={"width": "100%"},
                ),
            ],
            style=section_style,
        ),
        html.Div(
            [
                html.Button(
                    "Fetch Information",
                    id="submit-button",
                    n_clicks=0,
                    style={**button_style},  # Use button_style here
                ),
            ],
            style={
                **section_style,
                "border": "none",
            },  # Exclude border from button section
        ),
        html.Div(
            [
                html.H1(
                    "RESPONSE FROM AI:",
                    style={
                        "color": "#F08080",
                        "fontSize": "18px",
                        "textAlign": "left",
                        "fontWeight": "bold",
                    },
                ),
                html.Div(
                    id="output-container-button",
                    children="\n".join(response_list),
                    style={
                        "textAlign": "left",
                        "color": "#333333",
                        "whiteSpace": "pre-wrap",
                    },
                ),
            ],
            style=section_style,
        ),
    ]
)


def get_gemini_response(input, image, prompt):

    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text


def process_image(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded))
    return image


@app.callback(
    Output("output-container-button", "children"),
    [Input("submit-button", "n_clicks")],
    [
        State("input", "value"),
        State("upload-image", "contents"),
        State("upload-image", "filename"),
    ],
)
def update_output(n_clicks, input_value, contents, filename):
    if n_clicks > 0:
        if contents is not None:
            image = process_image(contents, filename)
            response = get_gemini_response(input_value, [image], input_value)
            response_list_time = (
                f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {response}\n'
            )
            response_list.insert(0, response_list_time)
            return response_list


if __name__ == "__main__":
    app.run_server(debug=True)
