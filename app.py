from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import hashlib

app = Flask(__name__)

# Directory where files are stored
FILES_DIRECTORY = "files" #"/app/files"
API_URL = "your.api.url"
HASH_EXTENSION = ".sha256"

def get_file_size_in_bytes(path):
    root = os.path.dirname(__file__)
    file_name = os.path.join(root, path)
    file_stats = os.stat(file_name)
    return file_stats.st_size

def get_sum_file_size_in_bytes(path_list):
    total_size = 0
    for path in path_list:
        total_size += get_file_size_in_bytes(path)
    return total_size

def get_files():
    file_list = []
    for root, _, files in os.walk(FILES_DIRECTORY):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, FILES_DIRECTORY)
            file_list.append(relative_path)  # Get full file path
    return file_list

def get_checksums():
    return list(filter(lambda filename: (filename.endswith(HASH_EXTENSION)), get_files()))

def get_data_files():
    return list(filter(lambda filename: (not filename.endswith(HASH_EXTENSION)), get_files()))

def check_sums():
    missing_sums = list(filter(lambda filename: (filename + HASH_EXTENSION) not in get_checksums(), get_data_files()))
    for missing_sum in missing_sums:
        generate_sum(missing_sum)

def generate_sum(file):
    file_hash = ""
    with open (FILES_DIRECTORY + "/" + file, "rb") as f:
        bytes = f.read()
        file_hash = hashlib.sha256(bytes).hexdigest()
    
    try:
        with open (FILES_DIRECTORY + "/" + file + HASH_EXTENSION, "x") as f:
            f.write(file_hash)
    except FileExistsError:
        print("Checksum already exists.")

def get_files_and_sums(version = None):
    
    root = os.path.dirname(__file__)
    file_and_sum_pairs = []    

    data_files = get_data_files()
    for file in data_files:
        f = open(FILES_DIRECTORY + "/" + file + HASH_EXTENSION, "r")
        print(root + "/" + FILES_DIRECTORY)
        path = os.path.join(root + "/" + FILES_DIRECTORY, file)
        file_and_sum_pairs.append({"path":file, "hash":f.read(), "bytes":get_file_size_in_bytes(path)})
    
    return file_and_sum_pairs

def split_file_and_path(filename):

    path = ""
    if filename.rfind("/") != -1:
        last_slash_index = filename.rindex("/") + 1
        path = filename[0:last_slash_index]
        filename = filename[last_slash_index:len(filename)]
    return path, filename

@app.route("/update", methods=["POST"])
def list_files():
    check_sums()

    try:
        data = request.get_json()
        if not data or "version" not in data:
            return jsonify({"status": "error", "message": "No version provided"}), 400
        version = data["version"]
        response = get_files_and_sums(version)
        return jsonify({"status": "success", "files": response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/files/<path:filepath>", methods=["GET"])
def download_file(filepath):
    try:
        path, filename = split_file_and_path(filepath)
        return send_from_directory(f"{FILES_DIRECTORY}/{path}" , filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "File not found"}), 404

@app.route('/chat', methods=['POST'])
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

        response = requests.post(API_URL, json=request_data, headers=headers, timeout=15)
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



