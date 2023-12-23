import os

import streamlit as st
import google.generativeai as genai


# Process and store Query and Response
def llm_function(query, model):
  #response model output
  response = model.generate_content(query)

  # Displaying the Assistant Message
  with st.chat_message("assistant"):
      st.markdown(response.text)


  # Storing the User Message
  st.session_state.messages.append(
      {
          "role":"user",
          "content": query
      }
  )


  # Storing the Assistant Message
  st.session_state.messages.append(
      {
          "role":"assistant",
          "content": response.text
      }
  )

def create_model(): 
  # Set Google API key
  os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]
  genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

  # Create the Model: Text model
  model = genai.GenerativeModel('gemini-pro')
  return model 



def main():
  st.title("Custom ChatBot")

  model=create_model()

  display_usr_inp = True

  # Initialize chat history
  if "messages" not in st.session_state:
      st.session_state.messages = [
          {
              "role":"ai",
              "content":"Ask me Anything"
          }
      ]

  # App rerun display 
  # Display chat messages from history on app rerun
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  # Accept user input
  if display_usr_inp:
    query = st.chat_input("How can I help you ?")


  # Calling the Function when Input is Provided
  if query:
      # Displaying the User Message
      with st.chat_message("user"):
          st.markdown(query)

      with st.spinner("Loading..."):
        display_usr_inp = False
        llm_function(query,model)
        display_usr_inp = True


if __name__=='__main__':
  main()
