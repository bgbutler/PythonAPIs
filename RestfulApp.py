from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def checkPostedData(postedData, functionName):
    """Ensure posted data is complete.

    Also check that x/y is not undefined

    """
    operations = ["add", "subtract", "multiply"]
    if (functionName in operations):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif (functionName == "divide"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"])==0:
            return 302
        else:
            return 200


class Add(Resource):
        """This is for adding using the POST methods.

        Inputs: Numbers

        Returns: Sum

        """

        def post(self):
            """Use the POST method."""
            # Ste 1: Get Posted Data:
            postedData = request.get_json()

            status_code = checkPostedData(postedData, "add")
            if (status_code != 200):
                retJson = {
                    "Message": "An error Happened",
                    "Status Code": status_code
                }
                return jsonify(retJson)

            # If I am here, then status_code == 200
            x = postedData["x"]
            y = postedData["y"]
            x = int(x)
            y = int(y)

            # Step 2: Add the posted data
            ret = x + y
            retMap = {
                'Message': ret,
                'StatusCode': 200
            }
            return jsonify(retMap)

        pass


class Subtract(Resource):
        """Subtract using the POST methods.

        Inputs: Numbers

        Returns: Difference

        """

        def post(self):
            """Use the POST method.

            Inputs: Numbers

            Returns: Difference

            """
            # Ste 1: Get Posted Data:
            postedData = request.get_json()

            status_code = checkPostedData(postedData, "subtract")
            if (status_code != 200):
                retJson = {
                    "Message": "An error Happened",
                    "Status Code": status_code
                }
                return jsonify(retJson)

            # If I am here, then status_code == 200
            x = postedData["x"]
            y = postedData["y"]
            x = int(x)
            y = int(y)

            # Step 2: Subtract the posted data
            ret = x - y
            retMap = {
                'Message': ret,
                'StatusCode': 200
            }
            return jsonify(retMap)


class Multiply(Resource):
        """Multiply using the POST methods.

        Inputs: Numbers

        Returns: Product

        """

        def post(self):
            """Use the POST method.

            Inputs: Numbers

            Returns: Difference

            """
            # Ste 1: Get Posted Data:
            postedData = request.get_json()

            status_code = checkPostedData(postedData, "multiply")
            if (status_code != 200):
                retJson = {
                    "Message": "An error Happened",
                    "Status Code": status_code
                }
                return jsonify(retJson)

            # If I am here, then status_code == 200
            x = postedData["x"]
            y = postedData["y"]
            x = int(x)
            y = int(y)

            # Step 2: Subtract the posted data
            ret = x * y
            retMap = {
                'Message': ret,
                'StatusCode': 200
            }
            return jsonify(retMap)


class Divide(Resource):
    """Divide using the POST methods.

    Inputs: Numbers

    Returns: Sum

    """

    def post(self):
        """Use the POST methods."""
        # Step 1: Get Posted Data:
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "divide")
        if (status_code != 200):
            retJson = {
                "Message": "An error Happened",
                "Status Code": status_code
                }
            return jsonify(retJson)

        # If I am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        # Step 2: Divide the posted data
        ret = (x * 1.0) / y
        retMap = {
            'Message': ret,
            'StatusCode': 200
            }
        return jsonify(retMap)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")


@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
