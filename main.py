import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.schemas import *

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
    if len(sys.argv)>2 and sys.argv[2]=="--verbose":
        prompt_tokens=response.usage_metadata.prompt_token_count #type: ignore
        response_tokens=response.usage_metadata.candidates_token_count #type: ignore
        print(f"User prompt: {prompt}\nPrompt tokens: {prompt_tokens} \nResponse tokens: {response_tokens}\n")

    #Default sys out
    if response.function_calls:
        for response_part in response.function_calls:
            print(f"Calling function: {response_part.name}({response_part.args})")
    print(response.text)

if __name__=="__main__":
    main()