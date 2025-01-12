from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__)

# Directory where files are stored
FILES_DIRECTORY = "/app/files"
API_URL = "http://roguedev.net:8080/v1/chat/completions"

@app.route("/api/files", methods=["GET"])
def list_files():
    try:
        # Get list of files in the directory
        files = [f for f in os.listdir(FILES_DIRECTORY) if os.path.isfile(os.path.join(FILES_DIRECTORY, f))]
        return jsonify({"status": "success", "files": files}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/files/<filename>", methods=["GET"])
def download_file(filename):
    try:
        return send_from_directory(FILES_DIRECTORY, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "File not found"}), 404

@app.route('/api/chat', methods=['POST'])
def post_message():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"status": "error", "message": "No message provided"}), 400

        message = data['message']
        headers = {"Content-Type": "application/json"}
        request_data = {
            "model": "falcon3-1b-instruct-abliterated",
            "messages": [
                {"role": "system", "content": "You're a NPC in a fantasy game.'"},
                {"role": "user", "content": message}
            ],
            "max_tokens": 32,
            "temperature": 0.7
        }

        response = requests.post(API_URL, json=request_data, headers=headers, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), 200

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"status": "error", "message": f"HTTP error: {http_err}"}), 500
    except requests.exceptions.RequestException as req_err:
        return jsonify({"status": "error", "message": f"Request error: {req_err}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/test_post', methods=['POST'])
def test_post():
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # Extract the text message
        if not data or 'message' not in data:
            return jsonify({"status": "error", "message": "No message provided"}), 400

        message = data['message']

        # Process the message (for this example, we'll just return it)
        print(f"Received message: {message}")

        #response = requests.post(API_URL, json=data, headers=headers)
        response = {"status": "ok", "message":f"You sent {message}"}

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

