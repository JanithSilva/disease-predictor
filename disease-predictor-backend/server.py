from flask import Flask, jsonify, request, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db.models import db, create_default_user
from route_blueprints.auth import auth_bp
from route_blueprints.route import route_bp
from flask_login import  LoginManager
from db.models import User
import redis

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

login_manager = LoginManager()
load_dotenv()

app = Flask(__name__)

CORS(app)  # Allow all origins

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Initialize LoginManager with the Flask app
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#registerig auth blueprint
app.register_blueprint(auth_bp)

#registerig route blueprint
app.register_blueprint(route_bp)


# Make Redis client available in blueprints
redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST'), 
    port=os.getenv('REDIS_PORT'), 
    db=0
)
auth_bp.redis_client = redis_client
route_bp.redis_client = redis_client


#Manually push the application context
with app.app_context():
    # Create all tables defined in models.py if they do not exist
    db.create_all()
    #create default user
    create_default_user()
    

@app.route('/', methods=['GET'])
def generate_question():
    return jsonify({"status": "working"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)