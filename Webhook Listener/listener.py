"""
listener.py
Version 1.0
Written by Asher Burrows

This script sets up a standalone Flask application to listen for webhook events and log patient admission data to the database.
The application is served using Waitress and is configured to be run as a Windows service using NSSM (Non-Sucking Service Manager).

Main Functions:
1. Configure Flask app and database settings.
2. Initialize database if not already present.
3. Define a webhook listener route to handle POST requests.

Usage:
- To run this script locally, execute it directly.
- For production use, set up an IIS reverse proxy to connect it to your domain and handle SSL offloading.
- Use NSSM to run this script as a Windows service.

Webhook Listener:
- Listens for POST requests with JSON payloads at /webhook.
- Verifies the event type is 'patient.admit'.
- Extracts patientId, facId, and eventDate from the payload.
- Logs the admission data to the NoAdmissions table.
- Returns a success response if the request is valid.
- Returns appropriate error responses for unsupported media types or methods.

To run as a Windows service using NSSM:
- Install NSSM: https://nssm.cc/download
- Command to install the service:
  nssm install AdmissionsWebhookListener "C:\path\to\python.exe" "C:\path\to\listener.py"
- Configure the service to start automatically and handle dependencies as needed.

Reverse Proxy with IIS:
- Set up a reverse proxy in IIS to forward requests from your domain to the local Flask app.
- Handle SSL offloading at the IIS level to secure the connection.

Example:
- Localhost URL: http://127.0.0.1:30440/webhook
"""

from datetime import datetime
from flask import Flask, request, abort, jsonify
from waitress import serve
import logging
from admissions_app import db, NoAdmissions, Config


app = Flask(__name__)
# set up dbs
app.config.from_object(Config)

# Verify the database URI
print('Database URI:', app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/webhook', methods=['POST'])
def webhook_listener():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            app.logger.debug('Webhook received: %s', data)

            # Check for patient.admit event
            if data.get('eventType') == 'patient.admit':
                try:
                    patientId = str(data.get('patientId'))
                    facId = str(data.get('facId'))
                    eventDate = datetime.fromisoformat(data.get('eventDate').replace('Z', '+00:00'))

                    # Create a new entry in NoAdmissions
                    new_entry = NoAdmissions(patientId=patientId, facId=facId, admissionDate=eventDate)
                    db.session.add(new_entry)
                    db.session.commit()
                    app.logger.info('New patient admission added: %s', data)

                except Exception as e:
                    app.logger.error('Error adding admission to database: %s', e)
                    db.session.rollback()
                    return jsonify({'status': 'error', 'message': str(e)}), 500

            return jsonify({'status': 'success'}), 200
        else:
            app.logger.error('Unsupported Media Type: %s', request.content_type)
            return 'Unsupported Media Type', 415
    else:
        return 'Method Not Allowed', 405


if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=30440)
