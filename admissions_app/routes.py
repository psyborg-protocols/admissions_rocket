from flask import render_template, request, jsonify
from . import app
import os
import json

# Use the test data if the environment variable USE_TEST_DATA is set to True
#if os.getenv('USE_TEST_DATA', 'False') == 'True':
#    from .test_pcc_api import fetch_patient_data
#else:
from .pcc_api import fetch_patient_data, get_oauth_token, fetch_facilities

@app.route('/')
def index():
    
    token = get_oauth_token()
    if token:
        patients_response = fetch_patient_data(token)
        if 'data' in patients_response:
            patients = patients_response['data']
            incomplete_patients = [p for p in patients if not p.get('admission_filled', False)]
            return render_template('index.html', patients=incomplete_patients)
        else:
            return "Failed to fetch patient data", 500
    else:
        return jsonify({"error": "Failed to obtain OAuth token"}), 50

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    patients_response = patient_fetcher()
    if 'data' in patients_response:
        patients = patients_response['data']
        filtered_patients = [p for p in patients if query.lower() in p.get('name', '').lower()]
        return jsonify(filtered_patients)
    else:
        return jsonify([])

@app.route('/submit_admission_form', methods=['POST'])
def submit_admission_form():
    data = request.get_json()
    patient_id = data['patient_id']
    # Integrate with MSBDocs API to prefill and redirect
    # Example URL (replace with actual implementation)
    msbdocs_url = f"https://msbdocs.com/form?patient_id={patient_id}"
    return jsonify({"url": msbdocs_url})


@app.route('/console')
def console():
    from .console import run_console
    run_console()
    return "Console executed. Check your output."



@app.route('/facilities', methods=['GET'])
def get_facilities():
    token = get_oauth_token()
    if token:
        facilities = fetch_facilities(token)
        if facilities:
            return jsonify(facilities)
        else:
            return jsonify({"error": "Failed to fetch facilities data"}), 500
    else:
        return jsonify({"error": "Failed to obtain OAuth token"}), 500
