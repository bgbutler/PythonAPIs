# this is a hello world file

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/hithere')
def hi_there_everyone():
    return "I just hit /hithere"


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/my_json')
def my_json():
    retJson = {
        'Name': 'Bryan',
        'Age': 49,
        "phones": [
            {
                "phoneName": "Iphone8",
                "phoneNumber": 11111
            },
            {
                "phoneName": "Nokia",
                "phoneNumber": 111121
            }
        ]
    }
    return jsonify(retJson)


@app.route('/add_two_nums', methods=["POST"])
def add_two_nums():
    """
    **Get x, y from the posted data.

    add z = x + y
        Prepare a JSON "z":z

    return:
        jsonify(map_prepared)

    """
    dataDict = request.get_json()
    if "y" not in dataDict:
        return "ERROR", 305

    x = dataDict["x"]
    y = dataDict["y"]
    # add z = x + y
    z = x + y

    # Prepare a JSON "z":z
    retJSON = {
        "z": z
    }

    return jsonify(retJSON), 200


if __name__ == "__main__":
        app.run(debug=True)
