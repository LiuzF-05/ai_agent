import os
import subprocess

def run_python_file(working_directory, file_path):

    #Creates the absolute file_path
    abs_file_path=os.path.abspath(os.path.join(working_directory, file_path))

    #Checks if the directory is in the pre defined working_directory
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory\n'
    
    #Checks if the file path exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found'
    
    #Checks if it's a python file    
    if not file_path[-3::]==".py":
        return f'Error: "{file_path}" is not a Python file'

    #Catch exceptions and return the stdout and stderr of the python file, as well as telling exit code in case of failure
    try:
        result=subprocess.run(["python3", abs_file_path], timeout=30, capture_output=True, cwd=working_directory)
        if not result.stderr and not result.stdout:
            return f"No output produced" 
        final=f"STDOUT: {result.stdout.decode("utf-8")}\nSTDERR: {result.stderr.decode("utf-8")}"
        if result.returncode!=0:
            final+=f"\nProcess exited with code {result.returncode}"  
        return final
    except Exception as e:
        return f'Error: Failed executing Python file {e}'