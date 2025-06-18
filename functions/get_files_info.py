import os

def get_files_info(working_directory, directory=None):
    
    dir_path=os.path.abspath(working_directory)

    if directory:
        dir_path=os.path.abspath(os.path.join(working_directory, directory))

    #Checks if the directory path leads to an actual directory
    if not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory\n'
        

    #Checks if the directory is in the pre defined working_directory
    elif not dir_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        
    
    #Return string
    result=("")
    try:
        for content in os.listdir(dir_path):
            result+=f"- {content}: file_size={os.path.getsize(os.path.abspath(os.path.join(dir_path, content)))}, is_dir={os.path.isdir(os.path.abspath(os.path.join(dir_path, content)))}\n"
        return result
    
    except Exception as e:
        return f'Error listing files: {e}'