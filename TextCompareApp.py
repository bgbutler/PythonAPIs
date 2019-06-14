"""App to handle NLP text similarity work.

Steps - register

Validate the user several ways

Compare text
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]


def UserExist(username):
    """Find out if the username is already in the system."""
    if users.find({"Username": username}).count == 0:
        return False
    else:
        return True


class Register(Resource):
    """Register the users information."""

    def post(self):
        """Register the users."""
        postedData = request.get_json(force=True)

        username = postedData["username"]
        password = postedData["password"]
        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username, choose another user name."
            }
        return jsonify

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.inser({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "You have successfully signed up for the API."
        }
        return jsonify(retJson)


def verifyPw(username, password):
    """Verify the username and password."""
    if not UserExist(username):
        return False

    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def countTokens(username):
    """Count the number of tokens the user has."""
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens


class Detect(Resource):
    """Get the posted data to check."""

    def post(self):
        """Post the data to the API."""
        postedData = request.get_json(force=True)
        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username."
            }
            return jsonify(retJson)

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "Invalid Password."
            }
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 303,
                "msg": "Sorry, you are out of tokens.  Please refill."
            }
            return jsonify(retJson)

        # calculate the edit distance using spacy
        nlp = spacy.load('en_core_web_sm')
        text1 = nlp(text1)
        text2 = nlp(text2)

        # looking for the ratio of similarity
        # ratio is a number from 0 to 1, higher is more similar
        ratio = text1.similarity(text2)
        # the reJson could be a function and just reused
        retJson = {
            "status": 200,
            "similarity": ratio,
            "msg": "Similarity score calculated successfully"
        }

        # deduct a token for using the service
        current_tokens = countTokens(username)
        users.update({
            "Username": username,
            "$set": {
                "Tokens": current_tokens-1
            }
        })
        return jsonify(retJson)


class Refill(Resource):
    """Perform refill of the tokens."""

    def post(self):
        """Post the refill data."""
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["refill"]
        if not UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)
        correct_pw = "abc123"
        if not password == correct_pw:
            retJson = {
                "status": 304,
                "msg": "Invalid Admin Password"
            }
            return jsonify(retJson)
        current_tokens = countTokens(username)
        users.update({
            "Username": username
        }, {
            "$set": {
                "Tokens": refill_amount + current_tokens
            }
        })

        retJson = {
            "status": 200,
            "msg": "Refilled successfully"
        }
        return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
