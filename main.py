import requests
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# Enable CORS for all domains
CORS(app)

# Initialize Flask-RESTx API
api = Api(
    app,
    version="1.0",
    title="Proxy API",
    description="A simple proxy server with Swagger UI",
)

# Define a namespace (groups endpoints in Swagger)
ns = api.namespace("proxy", description="Proxy operations")

# Define the input model for Swagger UI documentation
# This lets you test the API visually in the browser
input_model = api.model(
    "ProxyRequest",
    {
        "message": fields.String(required=True, description="The message to send"),
        "history": fields.List(fields.Raw, description="Conversation history"),
    },
)


@ns.route("")
class ProxyResource(Resource):
    @ns.expect(input_model)  # Uses the model defined above for Swagger input
    def post(self):
        """
        Forward request to target API (currently httpbin for testing)
        """
        try:
            # 1. Get the JSON payload (api.payload parses the body)
            incoming_data = api.payload

            # 2. Define target (httpbin for demo)
            target_url = "https://httpbin.org/post"

            # 3. Add headers (Simulating API key addition)
            headers = {
                "Content-Type": "application/json",
                "x-api-key": "Claude-anthropic-key",
            }

            # 4. Forward the request
            response = requests.post(target_url, json=incoming_data, headers=headers)

            # 5. Return the response
            return response.json(), response.status_code

        except Exception as e:
            return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
