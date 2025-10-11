import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.call_function import call_function, available_functions
def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions]
                    ),
                )
            for candidate in response.candidates:
                messages.append(candidate.content)
            if verbose:
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")

            if not response.function_calls:
                print(response.text)
                break

            function_responses = []
            for function_call_part in response.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                function_call_result = call_function(function_call_part, verbose)
                if (
                    not function_call_result.parts[0].function_response.response
                    or not function_call_result.parts
                    ):
                    raise Exception("Error: No function call")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                function_responses.append(function_call_result.parts[0])
                
                if not function_responses:
                    raise Exception("no function responses generated, exiting.")
            tool_msg = types.Content(role="user", parts=function_responses)
            messages.append(tool_msg)
        except Exception as e:
            print(f"Error: {e}")
            break


            



if __name__ == "__main__":
    main()
