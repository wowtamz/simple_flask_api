from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

# Directory where files are stored
FILES_DIRECTORY = "/app/files"
API_URL = "http://localhost:8080/v1/chat/completions"

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
        # Get JSON data from the POST request
        data = request.get_json()

        # Extract the text message
        if not data or 'message' not in data:
            return jsonify({"status": "error", "message": "No message provided"}), 400

        message = data['message']

        headers = {"Content-Type": "application/json"}
        
        data = {
            "model":"falcon3-1b-instruct-abliterated",
            "messages": [
                {"role": "system", "content": "You're a NPC in a fantasy game.'"},
                {"role": "user", "content": message}
            ],
            "max_tokens": 32,
            "temperature": 0.7
        }

        # Process the message (for this example, we'll just return it)
        print(f"Received message: {message}")

        response = requests.post(API_URL, json=data, headers=headers)

        # {"status": "success", "message": response}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

