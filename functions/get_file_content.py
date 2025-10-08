import os
from config import max_read_chars
def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    common_path = os.path.commonpath([target_file, abs_working_dir])
    if common_path != abs_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    # TODO: read file and store max 10000 chars for agent input
    try:
        with open(target_file) as f:
            file_content_string = f.read(max_read_chars)
            return file_content_string
    except Exception as e:
        return "Error: Error reading file"
    