import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv("apikey.env")
    api_key = os.environ.get("GEMINI_API_KEY")
    if len(sys.argv) < 2:
        print("Error: No prompt provided. Usage: python main.py \"Command line argument\"[--verbose]")
        sys.exit(1)
    
    args = sys.argv[1:]
    user_prompt = args[0]
    verbose = "--verbose" in args

    client = genai.Client(api_key=api_key)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages 
    )

    print("Hello from aiagent!")
    if verbose:
        print(f'User prompt: "{user_prompt}"')
    
    print(response.text)

    if response.usage_metadata and verbose:
        print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"\nResponse tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
