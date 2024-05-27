import streamlit as st
import requests
import extra_streamlit_components as stx
import json
from streamlit_option_menu import option_menu
from symptom import symptom_list, prepare_model_input


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
        
def check_backend_session_status(session_cookie):

    url = "http://localhost:5000/is_loggedin"

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'session={session_cookie}'
    }

    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return True
    else: 
        return False
    
# Function to make a POST request to the backend server for login
def login(username, password):
    url = "http://localhost:5000/login"
    
    data = {"username": username, "password": password}

    # Serialize data to JSON format
    json_data = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
        'Content-Encoding': 'gzip'           
    }

    response = requests.post(url, data=json_data, headers = headers)
    return response

# Function to make a POST request to the backend server for user registration
def register(username, password):
    # Replace this with your registration endpoint if different
    url = "http://localhost:5000/register"
    
    data = {"username": username, "password": password}

      # Serialize data to JSON format
    json_data = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',  
        'Content-Encoding': 'gzip'          
    }
    response = requests.post(url, data=json_data, headers = headers)
    return response

def clear_memory():
    url = "http://localhost:5000/agent/clear_memory"

    session_cookie = st.session_state.session_cookie

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'session={session_cookie}'
    }
    response = requests.post(url, headers = headers)
    return response

# Function to make a GET request to the backend server for logout
def logout():
    # Replace this with your logout endpoint if different
    url = "http://localhost:5000/logout"
    session_cookie = st.session_state.session_cookie
    headers = {
        'Content-Type': 'application/json',  
        'Content-Encoding': 'gzip',
        'Cookie': f'session={session_cookie}'          
    }
    response = requests.post(url, headers=headers)
    return response

def generate_question(answer_to_previous_question):
    url = "http://localhost:5000/agent/generate_question"
    session_cookie = st.session_state.session_cookie
    print(session_cookie)
    headers = {
        'Content-Type': 'application/json',
        'Cookie':f'session={session_cookie}',
    }

    data = {"patient": answer_to_previous_question}

    # Serialize data to JSON format
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers=headers)
    response_data = response.json()
    question = response_data.get("question")
    thought = response_data.get("thought")
    return question, thought

def diagnose():
    url = "http://localhost:5000/agent/diagnose"
    session_cookie = st.session_state.session_cookie
    headers = {
        'Cookie': f'session={session_cookie}'          
    }
  
    response = requests.post(url,headers=headers)
    response_data = response.json()
    return response_data

# Login page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = login(username, password)
        if response.status_code == 200:
            st.success("Login Successful!")
            # Store session cookie value in session state
            session_cookie = response.cookies.get("session")
            if session_cookie:
                st.session_state.session_cookie = session_cookie
                st.session_state.logged_in = True
                set_cookie("dp_session", session_cookie)
                st.write("Redirecting to Home Page...")
                # Redirect to Home Page
                home_page()
            else:
                st.error("Failed to obtain session cookie. Please try again.")
        else:
            st.error("Login Failed. Please check your credentials.")

# User registration page
def register_page():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        response = register(username, password)
        if response.status_code == 200:
            st.success("Registration Successful!")
            # Redirect to Login Page
            login_page()
        else:
            st.error("Registration Failed. Please try again.")

def home_page():
    empty_space_for_logout = 21
    with st.sidebar:
        selected = option_menu(
            menu_title=None, 
            options= ["Home", 'Disease Predictor','Chat'], 
            icons=['house', 'clipboard2-pulse-fill','chat'],
            menu_icon="cast",
            default_index=0)

        if selected == 'Chat':
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
                clear_memory()
                st.rerun()

            # Define a state variable to control whether to display diagnosis content
            if "show_diagnosis" not in st.session_state:
                st.session_state.show_diagnosis = False
                
            if right_column.button('Diagnose'):
                # Set the state variable to True when the "Diagnose" button is clicked
                st.session_state.show_diagnosis = True
            
            st.sidebar.markdown("---")

    if selected == 'Disease Predictor':
        # Allow users to select one or more options
        if "selected_options" not in st.session_state:
            st.session_state.selected_options = []
            
        selected_options = st.multiselect("Select symptoms:", options=symptom_list,default = st.session_state.selected_options)
        st.session_state.selected_options = selected_options
        model_input = prepare_model_input(selected_options)
        st.markdown(model_input)

    if selected == 'Chat':
        if not st.session_state.show_diagnosis:
           
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Accept user input
            if prompt := st.chat_input("What is up?"):
            # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)
            # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                #generating question
                with st.spinner("Thinking..."):
                    quesion, thought = generate_question(prompt)
                # Display assistant message in chat message container
                if quesion and prompt:
                    with st.chat_message("assistant"):
                        st.markdown(thought)
                        st.markdown(quesion)

            # Add user assistant to chat history
                st.session_state.messages.append({"role": "assistant", "content": thought})
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
                    results = diagnose()
                    st.session_state.diagnosis = results
            
            st.subheader('Differentials', divider='orange')
            st.markdown(st.session_state.diagnosis.get("differentials"))
            st.subheader('Indicators', divider='orange')
            st.markdown(st.session_state.diagnosis.get("indicators"))
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
            response = logout()
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