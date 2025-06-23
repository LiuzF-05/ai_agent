from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):

    #Defines the dictionary with all possible functions
    funct_dict={"get_files_info": get_files_info,
                "get_file_content": get_file_content,
                "write_file": write_file,
                "run_python_file": run_python_file,}
    
    #Adds a check for verbose, changing how much information is returned
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    if not function_call_part.name in funct_dict:
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)

    #Calling the actual function
    result=funct_dict[function_call_part.name](**{**function_call_part.args, 'working_directory': './calculator',})

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result },
        )
    ],
)