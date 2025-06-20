import os

def get_file_content(working_directory, file_path):
    
    #Creates the absolute file_path
    abs_file_path=os.path.abspath(os.path.join(working_directory, file_path))

    #Checks if the directory is in the pre defined working_directory
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory\n'
    
    #Checks if the file_path leads to a file    
    elif not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    #Catch exceptions and return the file's contents truncated at 10000 chars
    try:
        with open(abs_file_path, "r") as f:
            file_content=f.read(10000)
            if len(file_content)==10000:
                return f'{file_content}[...File "{file_path}" truncated at 10000 characters]'
        return file_content
    except Exception as e:
        return f'Error: Failed reading files {e}'