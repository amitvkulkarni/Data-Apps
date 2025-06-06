import os
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from helper import get_analysis, get_verdict_message, get_severity_label  



# ---------------------------------------------------------------------------
# Initialize Dash app with Bootstrap theme for enhanced UI
# ---------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Azure Content Safety Checker"


# ---------------------------------------------------------------------------
# App Layout: Main UI structure using Dash Bootstrap Components
# ---------------------------------------------------------------------------
app.layout = dbc.Container(
    html.Div([
        dbc.Row([
            dbc.Col(html.H2("🔍 Smart Content Risk Analyzer"), className="text-center my-4")
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Textarea(
                    id='input-text',
                    placeholder='Enter your text here...',
                    style={'height': '150px', 'resize': 'none'}
                ),
                dbc.Button('Analyze Text', id='analyze-btn', color="primary", className="mt-3"),
                html.Div(id='output-alert', className="mt-4"),
                html.Div(id='graph-container', className="mt-4")
            ], width=12)
        ])
    ],
    style={
        'border': '1px solid #dcdcdc',
        'borderRadius': '12px',
        'boxShadow': '2px 2px 8px rgba(0,0,0,0.05)',
        'padding': '30px',
        'backgroundColor': 'white'
    }),
    style={
        'maxWidth': '700px',
        'margin': '40px auto',
        'padding': '10px'
    },
    fluid=True
)

# ---------------------------------------------------------------------------
# Callback: Analyze text and update UI with verdict and severity chart
# ---------------------------------------------------------------------------
@app.callback(
    [Output('output-alert', 'children'),
     Output('graph-container', 'children')],
    [Input('analyze-btn', 'n_clicks')],
    [State('input-text', 'value')]
)
def analyze(n_clicks, input_text):
    """
    Callback to analyze the input text when the button is clicked.
    Displays a verdict alert and a severity bar chart if applicable.
    """
    if not input_text:
        return dbc.Alert("❗ Please enter some text.", color="info"), None

    analysis = get_analysis(input_text)
    if "error" in analysis:
        return dbc.Alert(f"Error: {analysis['error']}", color="danger"), None

    verdict = get_verdict_message(analysis)

    # If content is safe in all categories, skip the chart
    if all(score == 0 for score in analysis.values()):
        return verdict, None

    # Prepare horizontal bar chart for severity by category
    bars = go.Bar(
        y=list(analysis.keys()),
        x=list(analysis.values()),
        orientation='h',
        marker=dict(
            color=[
                'green' if val == 0 else
                'orange' if val <= 4 else
                'red' for val in analysis.values()
            ]
        ),
        text=[f"Severity: {val}" for val in analysis.values()],
        textposition='inside'
    )

    fig = go.Figure(data=[bars])
    fig.update_layout(
        title="Content Severity by Category",
        xaxis=dict(title="Severity (0–7)", range=[0, 7]),
        yaxis=dict(title="Category"),
        height=300,
        margin=dict(l=60, r=30, t=40, b=40)
    )

    return verdict, dcc.Graph(figure=fig)

# ---------------------------------------------------------------------------
# Main entry point: Run the Dash app
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)