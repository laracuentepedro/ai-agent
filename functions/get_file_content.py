import os
from config import max_read_chars
from google.genai import types
def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    common_path = os.path.commonpath([target_file, abs_working_dir])
    if common_path != abs_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file) as f:
            file_content_string = f.read(max_read_chars)
            return file_content_string
    except Exception as e:
        return "Error: Error reading file"
    
# Schema for instructing the Agent how to use this function tool
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_content",
    description="Retrieves the content for the specified file in the working directory, constrained to the working directory.",
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
        },
    ),
)