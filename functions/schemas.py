from google import genai
from google.genai import types

#Declares the get_files_info function, passing the parameters and description to the AI
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

#Declares the get_file_contents function, passing the parameters and description to the AI
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the contents in a file, truncating it to a maximum of 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to get the content from, relative to the working directory.",
            ),
        },
    ),
)

#Declares the write_files function, passing the parameters and description to the AI
schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Writes text into the selected file, creating it if there isn't one, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file that will be written, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=""
            )
        },
    ),
)

#Declares the run_python function, passing the parameters and description to the AI
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file that will be ran, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)