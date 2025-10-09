import os
from google.genai import types

# Purpose: Ensure guardrails for the agent so it never strays from the working directory
def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    full_target = os.path.join(working_directory, directory)
    abs_target = os.path.abspath(full_target)
    base = os.path.commonpath([abs_target, abs_working])
    if base != abs_working:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'
    
    try:
        dir_list = os.listdir(abs_target)
        lines = []
        for name in dir_list:
            p = os.path.join(abs_target, name)
            is_dir = os.path.isdir(p)
            size = os.path.getsize(p)
            lines.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')
        return '\n'.join(lines)
    except Exception as e:
        return f"Error: {e}"

# Schema for instructing the Agent how to use this function tool
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)