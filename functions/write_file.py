import os
from google.genai import types
def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    common_path = os.path.commonpath([abs_working_dir, target_file])
    if abs_working_dir != common_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    target_dir = os.path.dirname(target_file)
    try:
        os.makedirs(target_dir, exist_ok=True)
        with open (target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

# Schema for instructing the Agent how to use this function tool
schema_get_files_info = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the specified file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to retrieve the file from, relative to the working directory. Must be specified. Must be within the boundaries of the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to re-write the file with.",
            ),
        },
    ),
)