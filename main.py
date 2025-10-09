import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info

def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info]
    )
    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt")
        sys.exit(1)
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
            ),
        
        )
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)
    # TODO: Replace with argparse tools
    if len(sys.argv) > 2:
        if "--verbose" in sys.argv[2:]:
            print(f"User prompt: {user_prompt}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")



if __name__ == "__main__":
    main()
