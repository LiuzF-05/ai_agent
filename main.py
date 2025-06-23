import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.schemas import *
from call_function import call_function


#Defining system prompt to decide personality and behaviours
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

When in doubt of what the user might be referring to, use the tools to list the files and read the contents in order to find the most sensible match, letting the user know that it might be wrong due to prompt vagueness.

You should never ask the user for clarifications as that is outside of your scope. Simply look for the most logical match to what the user is asking.
"""

#List of available functions
available_functions=types.Tool(function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
    ])

def main():
    verbose=False

    #Loading the API key
    load_dotenv()
    api_key=os.environ.get("GEMINI_API_KEY")
    client=genai.Client(api_key=api_key)

    #Checking for user prompt
    if len(sys.argv)<2:
        print("Incorrect format (missing an argument)")
        sys.exit(1)
    prompt=sys.argv[1]

    #Checking for verbose
    if len(sys.argv)>2 and sys.argv[2]=="--verbose":
        verbose=True
        
    #List of previous messages
    messages=[types.Content(role="user", parts=[types.Part(text=prompt)])]

    #Function calling loop, limited to 20 calls to avoid infinite function loops
    for i in range(20):

        #Generating the prompt's response with the context of the messages list
        response=client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),)
        for candidate in response.candidates: #type:ignore
            messages.append(candidate.content) #type: ignore

        #If a function is called by the agent, it's result is added to the messages. In case of no output it will raise an error.
        if response.function_calls:
            for response_part in response.function_calls:
                funct_result=call_function(response_part, verbose)
                if "error" in funct_result.parts[0].function_response.response: #type: ignore
                    raise Exception ("Error: function did not generate a response")
                if verbose:
                    print(f"-> {funct_result.parts[0].function_response.response}") #type: ignore
                messages.append(funct_result)

        #Once the agent has stopped making calls it will break the loop and print the final response
        else:
            print(response.text)
            break

    #Checking for verbose arg and printing the required debug information
    if verbose:
        prompt_tokens=response.usage_metadata.prompt_token_count #type: ignore
        response_tokens=response.usage_metadata.candidates_token_count #type: ignore
        print(f"User prompt: {prompt}\nPrompt tokens: {prompt_tokens} \nResponse tokens: {response_tokens}\n")

if __name__=="__main__":
    main()