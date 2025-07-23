import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_files_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

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

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_run_python_file,
            schema_get_file_content,
            schema_write_file,
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    print("Hello from aiagent!")
    if verbose:
        print(f'User prompt: "{user_prompt}"')
    
    max_iterations = 20
    
    for step in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
            
                )
             )
            
            if verbose:
                print (f"\n--- Iteration {step + 1} ---")
            
            if response.text:
                print(response.text)
                

    
            if response.function_calls:
                for func_call in response.function_calls:
                    if verbose:
                        print(f"-> Received function call: {func_call.name}")
                    
                    tool_result = call_function(func_call, verbose=verbose)

                    messages.append(types.Content(role="model", parts=[types.Part(function_call=func_call)]))
                    messages.append(tool_result)

            if hasattr(response, "candidates"):
                for cand in response.candidates:
                    if cand.content:
                        messages.append(cand.content)
            
            if response.usage_metadata and verbose:
                print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        except Exception as e:
            print(f"[ERROR] {e}")
            break
    else:
        print("[INFO] Reached maximum iterations without a final response.")

        
        

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    func_args = dict(function_call_part.args)
    func_args["working_directory"] = "./calculator"

    print(f"[FUNCTION CALL] {function_name}({func_args})")

    func_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "run": run_python_file,
        "write_file": write_file,
    }

    if function_name not in func_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )

    function_result = func_map[function_name](**func_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )


if __name__ == "__main__":
    main()
