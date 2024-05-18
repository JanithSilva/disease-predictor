from flask import Blueprint, request, jsonify, session
from db.models import User
from flask_login import login_required, current_user
from llm_chatbot import run_QnA_agent_executer, prepare_medical_notes, disgnose
import pickle
from langchain.memory import ConversationBufferMemory
import json  


route_bp = Blueprint('route', __name__)

#route for generating question for the patient's input
@route_bp.route('/agent/generate_question', methods=['POST'])
@login_required
def generate_Q():
    input = request.json.get("patient")
    #deserializing memory object retrieved from the redis
    memory = pickle.loads(route_bp.redis_client.get(current_user.get_id()))
    print(memory)
    #generating question
    output = run_QnA_agent_executer(input, memory)
    
    #serializing updated memeory object using pickle before storing in session
    #session['memory'] = pickle.dumps(memory)
    route_bp.redis_client.set(current_user.get_id(), pickle.dumps(memory))
    return jsonify(output)

@route_bp.route('/agent/clear_memory', methods=['POST'])
@login_required
def clear_memory():
    session.pop('memory', None)
    #new conversation memory object for user
    memory = ConversationBufferMemory(ai_prefix = "medical assistant", human_prefix = "patient's response")
    
    #serializing memeory object using pickle before storing in redis
    route_bp.redis_client.set(current_user.get_id(), pickle.dumps(memory))
    session['memory'] = pickle.dumps(memory)

    return jsonify({"message": "Memory clearled successfully"}), 200


@route_bp.route('/agent/diagnose', methods=['POST'])
@login_required
def diagnose():
    #deserializing memory object retrieved from the redis
    memory = pickle.loads(route_bp.redis_client.get(current_user.get_id()))

    #get the diagnosis
    medical_notes =  prepare_medical_notes(memory)
    #generate diagnosis
    diagnosis = disgnose(medical_notes)

    # Create a dictionary representation of the diagnosis object
    diagnosis_dict = diagnosis.__dict__ if hasattr(diagnosis, "__dict__") else vars(diagnosis)

    # Include medical_notes in the response
    diagnosis_dict['medical_notes'] = medical_notes

    # Convert the dictionary to a JSON object
    response = json.dumps(diagnosis_dict, indent=4)
    return response, 200





