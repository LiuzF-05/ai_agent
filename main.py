import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

#Loading the API key
load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")
client=genai.Client(api_key=api_key)

#Checking for user prompt
if len(sys.argv)<2:
    print("Incorrect format (missing an argument)")
    sys.exit(1)
prompt=sys.argv[1]

#List of previous messages
messages=[types.Content(role="user", parts=[types.Part(text=prompt)])]

#Generating Gemini's response
response=client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

#Checking for verbose arg
if len(sys.argv)>2 and sys.argv[2]=="--verbose":
    prompt_tokens=response.usage_metadata.prompt_token_count #type: ignore
    response_tokens=response.usage_metadata.candidates_token_count #type: ignore
    print(f"User prompt: {prompt}\nPrompt tokens: {prompt_tokens} \nResponse tokens: {response_tokens}\n")

#Default sys out
print(response.text)