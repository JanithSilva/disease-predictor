import streamlit as st
import requests
import extra_streamlit_components as stx
import json
from streamlit_option_menu import option_menu
from symptom import symptom_list, prepare_model_input
from backend_requests import login, register, clear_memory, logout, generate_question, diagnose, get_top_predictions
import random

cookie_manager = stx.CookieManager()

# Placeholder for backend server URL
BACKEND_SERVER_URL = "http://localhost:5000"

def clear_cookie(key):
    cookie_manager.set(key, None)

def set_cookie(key, value):
    cookie_manager.set(key, value)

def get_cookie(key):
    cookie_value = cookie_manager.get(cookie=key)
    if cookie_value:
        return cookie_value
    else:
        return None

def login_page():
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            response = login(username, password)
            if response.status_code == 200:
                st.success("Login Successful!")
                session_cookie = response.cookies.get("session")
                if session_cookie:
                    st.session_state.session_cookie = session_cookie
                    st.session_state.logged_in = True
                    set_cookie("dp_session", session_cookie)
                    st.write("Redirecting to Home Page...")
                    home_page()
                else:
                    st.error("Failed to obtain session cookie. Please try again.")
            else:
                st.error("Login Failed. Please check your credentials.")
    
    with tab2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            response = register(username, password)
            if response.status_code == 201:
                st.success("Registration Successful!")
                # Redirect to Login Page
                login_page()
            else:
                response_data = response.json()
                st.error(f"Registration Failed. {response_data['message']}")




def home_page():
    empty_space_for_logout = 21
    with st.sidebar:
        selected = option_menu(
            menu_title=None, 
            options= [ 'Symptom Prediction','Chat with Assistant'], 
            # icons=['clipboard2-pulse-fill','chat'],
            # menu_icon="cast",
            default_index=0)

        if selected == 'Chat with Assistant':
            #space for logout button
            empty_space_for_logout = 9

            st.sidebar.markdown("---")

            left_column, right_column = st.columns(2)
            if left_column.button('Clear Chat'):
                #clearing messages, sessting state to show messages, removing diagnosis results
                st.session_state.messages = []
                st.session_state.show_diagnosis = False
                st.session_state.diagnosis = False

                #clearing backend memory
                clear_memory(st.session_state.session_cookie)
                st.rerun()

            # Define a state variable to control whether to display diagnosis content
            if "show_diagnosis" not in st.session_state:
                st.session_state.show_diagnosis = False
                
            if right_column.button('Diagnose'):
                # Set the state variable to True when the "Diagnose" button is clicked
                st.session_state.show_diagnosis = True
            
            st.sidebar.markdown("---")

    if selected == 'Symptom Prediction':
        # Allow users to select one or more options
        if "selected_options" not in st.session_state:
            st.session_state.selected_options = []
            
        selected_options = st.multiselect("Select symptoms:", options=symptom_list, default = st.session_state.selected_options)
        #st.session_state.selected_options = selected_options
        model_input = prepare_model_input(selected_options)
        
        if st.button("Predict"):
            with st.spinner("Please Wait..."):
                top_predictions = get_top_predictions(st.session_state.session_cookie, model_input)
                st.write("### Top Predictions:")
                for prediction in top_predictions:
                    st.write(f"- **{prediction['label']}**: {prediction['probability']:.2%}")
            
            if st.button("Clear"):
                st.session_state.selected_options = []
                st.experimental_rerun()  # Clear selections and refresh the page

    if selected == 'Chat with Assistant':
        if not st.session_state.show_diagnosis:
           
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []    

            if len(st.session_state.messages) == 0 :
                symptom_prompts = [
                    "Please share your symptoms.",
                    "What symptoms are you experiencing?",
                    "Can you tell me about your symptoms?",
                    "Please describe what you're feeling.",
                    "What symptoms do you have right now?",
                    "Could you provide details about your symptoms?",
                    "Let me know your symptoms for better assistance.",
                    "What specific symptoms are you noticing?"
                    ]

                # Select a random prompt
                random_prompt = random.choice(symptom_prompts)

                st.session_state.messages.append({"role": "assistant", "content": random_prompt})


            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Accept user input
            if prompt := st.chat_input(" "):
            # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)
            # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                #generating question
                with st.spinner("Thinking..."):
                    quesion, thought = generate_question(prompt, st.session_state.session_cookie)
                # Display assistant message in chat message container
                if quesion and prompt:
                    with st.chat_message("assistant"):
                        #st.markdown(thought)
                        st.markdown(quesion)

            # Add user assistant to chat history
                #st.session_state.messages.append({"role": "assistant", "content": thought})
                st.session_state.messages.append({"role": "assistant", "content": quesion})
                

        #rendering diagnosis results
        if st.session_state.show_diagnosis:
            # Display additional content for diagnosis
            st.title("Disease Prediction Results")
            #setting diagnosis state, if diagnose does not exist in session
            if "diagnosis" not in st.session_state :
                st.session_state.diagnosis = False

            if not st.session_state.diagnosis:
                with st.spinner("Operation in progress. Please wait."):
                    results = diagnose(st.session_state.session_cookie)
                    st.session_state.diagnosis = results
            
            st.subheader('Differentials', divider='orange')
            st.markdown(st.session_state.diagnosis.get("differentials"))
            st.subheader('Symptoms', divider='orange')
            st.markdown(st.session_state.diagnosis.get("symptoms"))
            st.subheader('Treatment', divider='orange')
            st.markdown(st.session_state.diagnosis.get("treatment"))
            st.subheader('Tests', divider='orange')
            st.markdown(st.session_state.diagnosis.get("tests"))
            st.subheader('Referrals', divider='orange')
            st.markdown(st.session_state.diagnosis.get("referrals"))
        
    # Empty space to push the logout button to the bottom
    for _ in range(empty_space_for_logout):
        st.sidebar.write("")

    if st.sidebar.button("logout"):
        try: 
            response = logout(st.session_state.session_cookie)
            if response.status_code == 200:
                #clear_cookie("dp_session")
                clear_cookie("dp_session")
                st.session_state.logged_in = False
                st.session_state.show_diagnosis = False
                st.session_state.diagnosis = False
                st.session_state.selected_options = []


                login_page()
        except Exception as e:
            login_page()
            st.error("Logout Failed!.")

# Main function to control the flow of the application
def main():
    if "session_cookie" not in st.session_state:
        session = get_cookie("dp_session")
        if(session is not None):
            st.session_state.session_cookie = session
    
    if "logged_in" not in st.session_state:
        login_page()
    else:
        if not st.session_state.logged_in:
            login_page()
        else:
            home_page()
        
      

if __name__ == "__main__":
    main()