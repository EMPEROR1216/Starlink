from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from comparable_agent import ComparableAgent

# Initialize Flask app and the agent
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)
agent = ComparableAgent()

print("--- Loading initial property data... ---")
industrial_data = agent.find_and_process_data()
if industrial_data.empty:
    print("--- WARNING: No data loaded. The API will not have property data. ---")
print("--- Data loaded successfully. API is ready. ---")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/properties', methods=['GET'])
def get_properties():
    if industrial_data.empty:
        return jsonify([])
    property_list = industrial_data[['property_identification_number']].to_dict(orient='records')
    return jsonify(property_list)

@app.route('/api/comparables/<string:pin>', methods=['GET'])
def get_comparables(pin):
    if industrial_data.empty:
        return jsonify({"error": "Data not loaded"}), 500
    
    comparables_df = agent.find_comparables(pin, industrial_data)
    result = comparables_df.to_dict(orient='records')
    return jsonify(result)

if __name__ == '__main__':
    print("--- STARTING FULL STARBOARD AGENT SERVER ---")
    app.run(debug=True, port=5001)