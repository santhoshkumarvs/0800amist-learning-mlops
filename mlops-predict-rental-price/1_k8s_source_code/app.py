from flask import Flask, request, jsonify, render_template
import subprocess
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests if needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.get_json()
    
    # Validate and convert the data if needed
    rooms_count = data.get('rooms_count')
    area_in_sqft = data.get('area_in_sqft')

    if rooms_count is None or area_in_sqft is None:
        return jsonify({"error": "Invalid input"}), 400

    # Write the data to the pipeline_args.json file
    with open('pipeline_args.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Trigger mlapp.py
    try:
        result = subprocess.run(['python', 'mlapp.py'], capture_output=True, text=True)
        return jsonify({"message": "Pipeline run submitted", "stdout": result.stdout, "stderr": result.stderr}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')