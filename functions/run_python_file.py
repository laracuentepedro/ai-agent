import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    common_path = os.path.commonpath([abs_working_dir, target_file])
    if common_path != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        full_args = ["python", target_file] + args
        completed_process = subprocess.run(
            full_args, 
            timeout=30, 
            capture_output=True,
            text=True,
            cwd=abs_working_dir
            )
        
        return_output = completed_process.stdout or "No output produced."
        return_statement = f"STDOUT: {return_output}, STDERR: {completed_process.stderr}"
        return_code = completed_process.returncode
        if return_code != 0:
            return_statement += f"Process exited with code {return_code}"
        return return_statement
    except Exception as e:
        return f"Error: executing Python file: {e}"