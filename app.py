from flask import Flask, jsonify, send_from_directory
from gpt4all import GPT4All
import os

app = Flask(__name__)

# Directory where files are stored
FILES_DIRECTORY = "/app/files"

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

        # Process the message (for this example, we'll just return it)
        print(f"Received message: {message}")

        answer = model.generate(message, max_tokens=512)

        return jsonify({"status": "success", "message": answer}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf", device="cpu") # downloads / loads a LLM
    with model.chat_session():
        print(model.generate("How can I run LLMs efficiently on my laptop?", max_tokens=1024))
    app.run(debug=True)

