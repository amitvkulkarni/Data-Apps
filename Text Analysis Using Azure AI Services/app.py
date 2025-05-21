import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Azure credentials
AZURE_KEY = os.getenv("AZURE_TEXT_ANALYTICS_KEY", "YOUR_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT", "YOUR_ENDPOINT")

def authenticate_client():
    credential = AzureKeyCredential(AZURE_KEY)
    client = TextAnalyticsClient(endpoint=AZURE_ENDPOINT, credential=credential)
    return client

client = authenticate_client()



# Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, 
                                                "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"],
                )

server = app.server

app.layout = dbc.Container([
    html.H1("InsightText: Real-Time Text Analytics", style={"color": "#007BFF", "fontWeight": "bold"}, className="text-center my-4"),

    dbc.Row([
        dbc.Col(
            dcc.Textarea(
                id='input-text',
                placeholder='Enter text to analyze...',
                style={'width': '100%', 'height': 150},
            ),
            width=12
        )
    ]),

    dbc.Row([
        dbc.Col(width=3),
        dbc.Col([
            dbc.Button("Analyze", id="analyze-button", color="primary", className="me-2"),
            dbc.Button("Clear", id="clear-button", color="secondary"),
        ], width="auto", className="d-flex justify-content-center"),
        dbc.Col(width=3)
    ], className="my-3"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                # dbc.CardHeader("Sentiment Analysis", style={"fontWeight": "bold"}),
                dbc.CardHeader([
                        html.I(className="bi bi-emoji-smile me-2 text-warning"),  # Bootstrap Icons
                         "Sentiment Analysis"
                    ], style={"fontWeight": "bold"}),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-sentiment",
                        type="default",
                        children=dcc.Graph(id='sentiment-graph', config={'displayModeBar': False})
                    )
                ])
            ])
        ], md=4),

        dbc.Col([
            dbc.Card([
                # dbc.CardHeader("Named Entities", style={"fontWeight": "bold"}),
                dbc.CardHeader([
                        html.I(className="bi bi-tags me-2 text-info"),
                        "Named Entities"
                    ],style={"fontWeight": "bold"}),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-entities",
                        type="default",
                        children=html.Ul(id='entities', style={'maxHeight': '300px', 'overflowY': 'auto'})
                    )
                ])
            ])
        ], md=4),

        dbc.Col([
            dbc.Card([
                # dbc.CardHeader("Key Phrases", style={"fontWeight": "bold"}),
                dbc.CardHeader([
                        html.I(className="bi bi-lightbulb me-2 text-success"),
                        "Named Entities"
                    ],style={"fontWeight": "bold"}),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-phrases",
                        type="default",
                        children=html.Ul(id='key-phrases', style={'maxHeight': '300px', 'overflowY': 'auto'})
                    )
                ])
            ])
        ], md=4),
    ], className="mt-3")
], fluid=True)


@app.callback(
    [
        Output('sentiment-graph', 'figure'),
        Output('entities', 'children'),
        Output('key-phrases', 'children'),
        Output('input-text', 'value'),
    ],
    [
        Input('analyze-button', 'n_clicks'),
        Input('clear-button', 'n_clicks')
    ],
    State('input-text', 'value'),
    prevent_initial_call=True
)
def handle_buttons(analyze_clicks, clear_clicks, text):
    ctx = dash.callback_context
    if not ctx.triggered:
        return default_fig(), default_list(), default_list(), ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'clear-button' or not text.strip():
        return default_fig(), default_list(), default_list(), ""

    try:
        sentiment_response = client.analyze_sentiment(documents=[text])[0]
        scores = sentiment_response.confidence_scores
        sentiment = sentiment_response.sentiment

        sentiment_fig = go.Figure(go.Pie(
            labels=['Positive', 'Neutral', 'Negative'],
            values=[scores.positive, scores.neutral, scores.negative],
            marker=dict(colors=['green', 'gray', 'red']),
            hole=0.4
        ))
        sentiment_fig.update_layout(
            title=f"Sentiment: {sentiment.capitalize()}",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True
        )

        entities_response = client.recognize_entities(documents=[text])[0]
        entities_list = [html.Li(f"{entity.text} ({entity.category})") for entity in entities_response.entities]
        if not entities_list:
            entities_list = default_list()

        key_phrases_response = client.extract_key_phrases(documents=[text])[0]
        key_phrases_list = [html.Li(phrase) for phrase in key_phrases_response.key_phrases]
        if not key_phrases_list:
            key_phrases_list = default_list()

        return sentiment_fig, entities_list, key_phrases_list, text

    except Exception as e:
        error_message = f"Error: {str(e)}"
        error_li = [html.Li(error_message)]
        return default_fig(error_message), error_li, error_li, text


def default_fig(message="No text available for analysis"):
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16),
        xref="paper", yref="paper"
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=250,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

def default_list():
    return [html.Li("No text available for analysis")]


if __name__ == '__main__':
    app.run(debug=True)
