from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

# Directory where files are stored
FILES_DIRECTORY = "./files"

@app.route("/api/files", methods=["GET"])
def list_files():
    try:
        # Get list of files in the directory
        files = [f for f in os.listdir(FILES_DIRECTORY) if os.path.isfile(os.path.join(FILES_DIRECTORY, f))]
        return jsonify({"status": "success", "files": files}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

