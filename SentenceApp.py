"""
This is an API.

This is for Registration of a users
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve the stored sentence on the database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

# db must be the same as in the docker-compose file
client = MongoClient("mongodb://db:27017")

db = client.SentencesDatabase
# make a collection called sentences
users = db["Users"]


class Register(Resource):
    """Set up the registration information."""

    def post(self):
        """Use the POST method."""
        # Ste 1: Get Posted Data by the user
        postedData = request.get_json(force=True)

        # Get the data
        username = postedData['username']
        password = postedData['password']

        # hash the password = password + salt
        # Hash a password for the first time, with a randomly-generated salt
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # store the username and password into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "You succesfully signed up for the API"
        }
        return jsonify(retJson)


def verifyPW(username, password):
        """Verify the user's password."""

        hashed_pw = users.find({
            "Username": username
        })[0]["Password"]
        # Check that an unencrypted password matches one that has
        # previously been hashed
        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            return True
        else:
            return False


def countTokens(username):
    """Count the tokens."""
    tokens = users.find({
            "Username": username
        })[0]["Tokens"]
    return tokens


class Store(Resource):
    """Store the user's data in the database."""

    def post(self):
        """Post the data."""
        # step 1 get the posted data
        postedData = request.get_json(force=True)

        # Step 2 is to read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        # Step 3 verify the username and pw match
        correct_pw = verifyPW(username, password)
        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)

        # Step 4 Verify the user has enought tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "msg": "Not enough tokens."
            }
            return jsonify(retJson)

        # Step 5 store the sentence, take 1 token,  and return code 200, OK
        users.update({
            "Usename": username
        }, {
            "$set": {
                "Sentence": str(sentence),
                "Tokens": num_tokens - 1
            }
        })
        retJson = {
            "status": 200,
            "msg": "Sentence saved successfully"
        }
        return jsonify(retJson)


class Get(Resource):
    """This gets the data."""

    def post(self):
        """Retrieve the data."""
        postedData = request.get_json(force=True)

        # get the user name and password
        username = postedData["username"]
        password = postedData["password"]
        # verify the password
        correct_pw = verifyPW(username, password)
        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)
        # verify tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)
        # get the data
        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "sentence": str(sentence)
        }
        return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
