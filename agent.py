import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import prompts
import json
# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

def query_gemini(prompt: str) -> str:
    if not client:
        raise RuntimeError("GEMINI_API_KEY not found or client not initialized.")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        ),
    )
    # Collect all text parts
    result = []
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text') and part.text is not None:
            result.append(part.text)
        if hasattr(part, 'executable_code') and part.executable_code is not None:
            result.append(part.executable_code.code)
        if hasattr(part, 'code_execution_result') and part.code_execution_result is not None:
            result.append(str(part.code_execution_result.output))
    return '\n'.join(result)

def generate_search_queries(user_input: str) -> str:
    prompt = prompts.make_search_query_prompt(user_input)
    result =query_gemini(prompt)
    start = str(result).find('{')
    end = str(result).rfind('}') + 1
    result = str(result)[start:end]
    #parse the result into list of search queries, only the values of the json that are not empty
    result_json = json.loads(result)
    search_queries = [query for query in result_json.values() if query]
    return search_queries


if __name__ == "__main__":
    print(generate_search_queries("10 עגבניות מגי"))