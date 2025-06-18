import os

def write_files(working_directory, file_path, content):

    #Creates the absolute file_path
    abs_file_path=os.path.abspath(os.path.join(working_directory, file_path))

    #Checks if the directory is in the pre defined working_directory
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory\n'
    
    #Defines the directory name of the file
    dir_name=os.path.dirname(abs_file_path)
    
    #Catch exceptions, create the necessary directories, write the file and return a string relaying whether it was succesful
    try:

    #Creates a directory if none exists
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing files {e}'
