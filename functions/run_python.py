import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command line arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python script.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    working_directory = os.path.abspath(working_directory)

    # Make sure file_path is relative, as expected by subprocess with cwd
    original_path = file_path
    full_path = os.path.abspath(os.path.join(working_directory, original_path))

    if os.path.commonpath([full_path, working_directory]) != working_directory:
        return f'Error: Cannot execute "{original_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'File "{original_path}" not found.'

    if not original_path.endswith(".py"):
        return f'Error: "{original_path}" is not a Python file.'

    try:
        command = ["python", file_path] + args  

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_directory,  
            timeout=30,
            text=True
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if not stdout and not stderr:
            return "No output produced."

        combined_output = (stdout + "\n" + stderr).strip()
        if not combined_output:
            return "No output produced."
        return combined_output

    except Exception as e:
        return f"Error: {str(e)}"
