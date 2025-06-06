import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import dash_bootstrap_components as dbc

# ---------------------------------------------------------------------------
# Load environment variables and initialize Azure Content Safety client
# ---------------------------------------------------------------------------
load_dotenv()
key = os.getenv("CONTENT_SAFETY_KEY")
endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")

client = None
client_init_error = None
try:
    if not key or not endpoint:
        raise ValueError("Azure Content Safety key or endpoint not set in environment variables.")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
except Exception as e:
    client_init_error = str(e)

# ---------------------------------------------------------------------------
# Helper function: Map severity score to human-readable label
# ---------------------------------------------------------------------------
def get_severity_label(score):
    """
    Returns a label for the given severity score.
    """
    if score == 0:
        return "✅ Safe"
    elif score <= 2:
        return "⚠️ Mild"
    elif score <= 4:
        return "⚠️ Moderate"
    else:
        return "🚫 High"

# ---------------------------------------------------------------------------
# Helper function: Analyze text using Azure Content Safety API
# ---------------------------------------------------------------------------
def get_analysis(text):
    """
    Calls Azure Content Safety API to analyze the input text.
    Returns a dictionary of category: severity or an error message.
    """
    if client_init_error:
        return {"error": f"Client initialization failed: {client_init_error}"}
    if not text or not isinstance(text, str):
        return {"error": "Input text must be a non-empty string."}
    try:
        response = client.analyze_text(AnalyzeTextOptions(text=text))
        return {cat.category: cat.severity for cat in response.categories_analysis}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

# ---------------------------------------------------------------------------
# Helper function: Generate verdict message based on analysis
# ---------------------------------------------------------------------------
def get_verdict_message(analysis):
    """
    Returns a Dash Bootstrap Alert component with a verdict message
    based on the severity scores in the analysis.
    """
    if "error" in analysis:
        return dbc.Alert(f"Error: {analysis['error']}", color="danger")
    if any(score >= 5 for score in analysis.values()):
        return dbc.Alert("🚫 Highly Harmful Content Detected", color="danger")
    elif any(score >= 3 for score in analysis.values()):
        return dbc.Alert("⚠️ Moderately Harmful Content", color="warning")
    else:
        return dbc.Alert("✅ Content is Safe", color="success")
