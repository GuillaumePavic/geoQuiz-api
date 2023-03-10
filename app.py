import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_expects_json import expects_json
from jsonschema import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from services.Quiz import Quiz
from services.User import User, createUserSchema, loginSchema

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)


# --- Quiz ---#
@app.get("/quiz")
def createQuiz():
    try:
        category = request.args.get('category')
        level = request.args.get('level')

        results = Quiz.getData(category, level)
        if len(results) == 0:
            return jsonify({"message": "Error 404, No Quiz Found !"})
            
        return {"results": results}
    except:
        return {"message": "Error 500"}


# --- User ---#
@app.post("/user")
@expects_json(createUserSchema)
def createUser():
    try:
        data = request.get_json()

        email = data['email']
        password = data['password']
        username = data['username']

        password_hashed = generate_password_hash(password)

        User.createUser(email, password_hashed, username)

        return {"message": "user created"}
    except:
        return {"message": "Error 500"}


@app.post("/user/login")
@expects_json(loginSchema)
def login():
    try:
        data = request.get_json()

        email = data['email']
        password = data['password']

        user = User.getUser(email)
        if user is None: 
            return {"message": "Error 400. Wrong email or password"}

        correctPassword = check_password_hash(user["password"], password)
        if correctPassword is False:
            return {"message": "Error 400. Wrong email or password"}
        
        encoded = jwt.encode({"id": user["id"], "isAdmin": user["isAdmin"]}, os.environ.get("JWT_SECRET"), algorithm="HS256")
        
        return {"message": encoded}
    except:
        return {"message": "Error 500"}


# Add country in DB
@app.post('/admin/addcountry')
def addCountry():
    try:
        jwtToken = request.headers['auth']
        if jwtToken is None:
            return {"message": "No token provided"}
        
        decoded = jwt.decode(jwtToken, os.environ.get("JWT_SECRET"), algorithms="HS256")
        if decoded["isAdmin"] is False:
            return {"message": "Not authorized"}
        
        # Add country
        return {"message": "Authorized"}
    except:
        return {"message": "Error 500"}


#--- Error Handling---#
@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return jsonify({'error': original_error.message})

    return error

@app.errorhandler(404) 
def invalid_route(e): 
    return jsonify({"message": "Error 404, Nothing to see here !"})