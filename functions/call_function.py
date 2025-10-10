from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from google.genai import types
from config import working_dir

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    func_map = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "write_file": write_file,
            "run_python_file": run_python_file
        }
    if function_call_part.name not in func_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    args_dict = function_call_part.args.copy()
    args_dict["working_directory"] = working_dir
    func_call_result = func_map[function_call_part.name](**args_dict)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": func_call_result},
        )
    ],
)

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
)
