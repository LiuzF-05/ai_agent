import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.schemas import *

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

def main():
    #Loading the API key
    load_dotenv()
    api_key=os.environ.get("GEMINI_API_KEY")
    client=genai.Client(api_key=api_key)

    #Defining system prompt to decide personality and behaviours
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    #Checking for user prompt
    if len(sys.argv)<2:
        print("Incorrect format (missing an argument)")
        sys.exit(1)
    prompt=sys.argv[1]

    #List of previous messages
    messages=[types.Content(role="user", parts=[types.Part(text=prompt)])]

    #List of available functions
    available_functions=types.Tool(function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
        ])

    #Generating Gemini's response
    response=client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),)

    #Checking for verbose arg
    verbose=False
    if len(sys.argv)>2 and sys.argv[2]=="--verbose":
        verbose=True
        prompt_tokens=response.usage_metadata.prompt_token_count #type: ignore
        response_tokens=response.usage_metadata.candidates_token_count #type: ignore
        print(f"User prompt: {prompt}\nPrompt tokens: {prompt_tokens} \nResponse tokens: {response_tokens}\n")

    #Default sys out
    if response.function_calls:
        for response_part in response.function_calls:
            funct_result=call_function(response_part, verbose)
            if "error" in funct_result.parts[0].function_response.response: #type: ignore
                raise Exception ("Error: function did not generate a response")
            if verbose:
                print(f"-> {funct_result.parts[0].function_response.response}") #type: ignore
        print(response.text)
    

    else:            
        print(response.text)

if __name__=="__main__":
    main()