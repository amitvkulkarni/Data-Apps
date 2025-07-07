import os
import google.generativeai as genai
import json
import re


def configure_llm():
    """Configures the generative AI model with the API key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)


def get_filters_from_llm(text_query):
    """Uses the LLM to extract filters from a text query."""
    configure_llm()
    model = genai.GenerativeModel("gemini-2.5-pro")

    # A very specific, few-shot prompt to guide the model to return valid JSON.
    prompt_template = """Your task is to act as a JSON extractor. You will be given a user query for finding Airbnb listings. You must extract the filtering criteria and respond with ONLY a single, valid JSON object. Do not include any other text, explanations, or markdown formatting.

    The JSON object must have the following keys: "neighbourhood_group", "neighbourhood", "room_type", "price_min", "price_max".
    The values for "room_type" must be one of: "Entire home/apt", "Private room", "Shared room".
    If a value is not present in the query, use null for that key.


    Query: "{query}"
    Response:"""

    prompt = prompt_template.replace("{query}", text_query)

    try:
        response = model.generate_content(prompt)
        response_text = response.text
        print("LLM Raw Response:", response_text)

        # The model should be returning only JSON, so we can try to parse it directly.
        try:
            filters = json.loads(response_text)
            return filters
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from LLM response: {e}")
            print(f"Received: {response_text}")
            # As a fallback, try to find JSON within the text.
            match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if match:
                try:
                    filters = json.loads(match.group(0))
                    return filters
                except json.JSONDecodeError as e_fallback:
                    print(f"Fallback JSON parsing also failed: {e_fallback}")
                    print(f"Extracted string: {match.group(0)}")
                    return None
            return None

    except Exception as e:
        print(f"An unexpected error occurred while calling the LLM: {e}")
        return None
