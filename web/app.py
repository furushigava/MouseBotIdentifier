import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import os
import argparse

app = Flask(__name__)
CORS(app, resources={r"/save_mouse_data_*": {"origins": "*"}})

DATA_DIR = 'data'

def append_data_to_file(data, filename):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    file_path = os.path.join(DATA_DIR, filename)
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as file:
                existing_data = pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
            existing_data = []
    else:
        existing_data = []

    existing_data.extend(data)

    with open(file_path, 'wb') as file:
        pickle.dump(existing_data, file)

def create_filename(base_name, site_url):
    # Замена всех неалфавитно-цифровых символов на _
    site_name = re.sub(r'\W+', '_', site_url)
    return f"{base_name}_{site_name}.pkl"

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/check_model')
def model():
    return render_template('model.html')

@app.route('/save_mouse_data_<type>', methods=['POST'])
def save_mouse_data(type):
    payload = request.get_json()
    data = payload.get('data')
    site_url = payload.get('siteURL')

    if data and site_url:
        base_name = args.file_name_bot if type == "bot" else args.file_name_browser
        filename = create_filename(base_name, site_url)
        append_data_to_file(data, filename)
        return jsonify({'status': 'success', 'message': 'Data saved successfully'}), 200
    
    return jsonify({'status': 'error', 'message': 'No data or site URL received'}), 400

@app.route('/batch_counts', methods=['GET'])
def batch_counts():
    def count_batches(filename):
        file_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(file_path):
            return 0
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
        return len(data)

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_names = [f for f in os.listdir(DATA_DIR) if f.startswith(args.file_name_bot) or f.startswith(args.file_name_browser)]
    counts = {}

    for file_name in file_names:
        count = count_batches(file_name)
        counts[file_name] = count

    return jsonify(counts), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask server to handle mouse data.")
    parser.add_argument('--file_name_bot', type=str, default='mouse_positions_bot', help='Base name of the file to store bot mouse data')
    parser.add_argument('--file_name_browser', type=str, default='mouse_positions_browser', help='Base name of the file to store browser mouse data')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the Flask server on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the Flask server on')

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
