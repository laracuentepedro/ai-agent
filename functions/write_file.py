import os
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

