import os

# Purpose: Ensure guardrails for the agent so it never strays from the working directory
def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_path)
    base = os.path.commonpath([abs_path, abs_working])
    if base != abs_working:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        dir_list = os.listdir(abs_path)
        lines = []
        for name in dir_list:
            p = os.path.join(abs_path, name)
            is_dir = os.path.isdir(p)
            size = os.path.getsize(p)
            lines.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')
        return '\n'.join(lines)
    except Exception as e:
        return f"Error: {e}"
