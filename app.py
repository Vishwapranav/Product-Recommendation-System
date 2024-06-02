import os.path
import streamlit as st
import pprint
import google.generativeai as genai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.generativeai as genai

SCOPES = ['https://www.googleapis.com/auth/generative-language.tuning']

def load_creds():
    """Converts `oauth-client-id.json` to a credential object.

    This function caches the generated tokens to minimize the use of the
    consent screen.
    """
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
  
def response_ai(inp):
    creds = load_creds()
    genai.configure(credentials=creds)
    models=[m.name for m in genai.list_tuned_models()]
    print()
    print('Available base models:', models)
    print('My tuned models:', [m.name for m in genai.list_tuned_models()])
    
    generation_config = {
      "temperature": 0,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 8192,
    }

    safety_settings = [
    ]

    model = genai.GenerativeModel(model_name=models[1],
                              generation_config=generation_config,
                              safety_settings=safety_settings)

    prompt_parts = [inp]

    response = model.generate_content(prompt_parts)
    return response.text

def main():

    ##
    st.set_page_config(page_title="Ecom PR system")
    st.header("Ecommerce Product Recommendation System")

    input=st.text_input("Input: ",key="input")
    submit=st.button("Ask the question")
    output=response_ai(input)
    if submit and input:
        st.write(output)
    
                
if __name__ == "__main__":
    main()