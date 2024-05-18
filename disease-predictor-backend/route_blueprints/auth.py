from flask import Blueprint, request, current_app, jsonify, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from db.models import User
from flask_login import login_user, login_required, logout_user, current_user
import pickle
from langchain.memory import ConversationBufferMemory

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json  
    username = data.get("username")
    password = data.get("password")

    # Validate username
    if not username:
        return jsonify({"message": "Username is required."}), 400
    elif len(username) < 4 or len(username) > 20:
        return jsonify({"message": "Username must be between 4 and 20 characters."}), 400
    
    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists."}), 400

    # Validate password
    if not password:
        return jsonify({"message": "Password is required."}), 400
    elif len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters long."}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Create a new user instance
    new_user = User(username=username, password=hashed_password)

    # Add the user to the database
    current_app.db.session.add(new_user)
    current_app.db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201



@auth_bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == "GET":
        return jsonify({"message": "Hello world from backend!, You nedd to login frist :-)"}), 400
    
    data = request.json  
    username = data.get("username")
    password = data.get("password")

    # Check if the username exists
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "Invalid username"}), 401

    # Check if the password is correct
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    # Log the user in
    login_user(user)

    #keep different conversation memory object for every user
    memory = ConversationBufferMemory(ai_prefix = "medical assistant", human_prefix = "patient's response")
    
    #serializing memeory object using pickle before storing in redis
    auth_bp.redis_client.set(current_user.get_id(), pickle.dumps(memory))
    #session['memory'] = pickle.dumps(memory)
    return jsonify({"message": "Logged in successfully"}), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    # Log out the user
    logout_user()

    # Clear any other session data
    session.clear()

    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/is_loggedin', methods=['POST'])
def protected():
    # Add the data to the redis
    if current_user.is_authenticated:
        message = "You are authenticated" 
        return jsonify({'message': message}), 200
    else:
        abort(400, 'User is not logged in')
    














       
   


