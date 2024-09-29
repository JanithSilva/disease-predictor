import json
import requests

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


def clear_memory(session_cookie):
    url = "http://localhost:5000/agent/clear_memory"

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'session={session_cookie}'
    }
    response = requests.post(url, headers = headers)
    return response

# Function to make a GET request to the backend server for logout
def logout(session_cookie):
    # Replace this with your logout endpoint if different
    url = "http://localhost:5000/logout"
    headers = {
        'Content-Type': 'application/json',  
        'Content-Encoding': 'gzip',
        'Cookie': f'session={session_cookie}'          
    }
    response = requests.post(url, headers=headers)
    return response

def generate_question(answer_to_previous_question, session_cookie):
    url = "http://localhost:5000/agent/generate_question"
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


def diagnose(session_cookie):
    url = "http://localhost:5000/agent/diagnose"
    headers = {
        'Cookie': f'session={session_cookie}'          
    }
  
    response = requests.post(url,headers=headers)
    response_data = response.json()
    return response_data

def get_top_predictions(session_cookie, model_input):
    url = "http://localhost:5000/predict"
    headers = {
        'Cookie': f'session={session_cookie}'          
    }
    data = {"model_input": model_input}
    # json_data = json.dumps(data)

    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    return response_data