import os
from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_dir_abs = os.path.abspath(working_directory)

        if not full_path.startswith(working_dir_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_size = os.path.getsize(full_path)

        with open(full_path, "r", encoding="utf-8") as f:
            if file_size > MAX_CHARS:
                content = f.read(MAX_CHARS)
                truncated_message = f"\n[...File '{file_path}' truncated at {MAX_CHARS} characters]"
                return content + truncated_message
            else:
                content = f.read()
                return content

    except Exception as e:
        return f"Error: {str(e)}"

