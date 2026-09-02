import os
from flask import Flask, request, jsonify
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

app = Flask(__name__)

project = AIProjectClient(
    endpoint="https://edufilho43-6512-ia-resource.services.ai.azure.com",
    credential=DefaultAzureCredential(),
)
client = project.get_openai_client()

@app.route("/protocols/openai/responses", methods=["POST"])
def respond():
    data = request.json or {}
    user_input = data.get("input", "")

    response = client.responses.create(
        model="gpt-5-nano",
        input=[{"role": "user", "content": user_input}]
    )
    
    return jsonify({"output_text": response.output_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)