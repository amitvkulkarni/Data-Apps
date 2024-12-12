from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os, openai

# Initialize the FastAPI app
app = FastAPI()


# LLMWrapper class (reuse from above)
class LLMWrapper:
    def __init__(self, m_name: str, api_key: str):
        self.m_name = m_name
        openai.api_key = api_key

    def _preprocess_input(self, user_input: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]

    def _postprocess_output(self, response: dict[str, str]) -> str:
        # return response["choices"][0]["message"]["content"].strip()
        return response

    def query(self, user_input: str) -> str:
        preprocessed_input = self._preprocess_input(user_input)
        try:
            response = openai.chat.completions.create(
                model=self.m_name,
                messages=preprocessed_input,
                max_tokens=100,
            )
            return self._postprocess_output(response)
        except Exception as e:
            return f"Error occurred: {str(e)}"


# Pydantic model for input validation
class QueryRequest(BaseModel):
    query: str
    m_name: Optional[str] = "gpt-3.5-turbo"  # Default model


# Initialize the LLMWrapper (set your OpenAI API key)
llm_wrapper = LLMWrapper(m_name="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))


@app.post("/query/")
async def get_llm_response(request: QueryRequest):
    """Endpoint to handle user queries."""
    try:
        # Use the LLMWrapper to get the model's response
        response = llm_wrapper.query(request.query)
        return {"query": request.query, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    """Basic endpoint to check if the API is running."""
    return {
        "message": "Welcome to the LLM API. Use POST /query/ to interact with the model."
    }
