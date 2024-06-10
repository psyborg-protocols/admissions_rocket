import requests
import base64
import logging

PCC_API_BASE_ENDPOINT = "https://connect2.pointclickcare.com/api/public/preview1/orgs"
ORGANIZATION_ID = "7daf45ae-1982-4b95-9df8-46a067df0de7"
PCC_CLIENT_ID = "DRM15QApMHlB8zzrh6HDGbgZ76bONQ6c"
PCC_CLIENT_SECRET = "olcYtZU1bdoxnl7q"
TOKEN_ENDPOINT = "https://connect.pointclickcare.com/auth/token"
CERT_FILE = "C:/Users/aburrows/Documents/Security/Client Certificate/admissionsrocket.xyz-chain.pem"
KEY_FILE = "C:/Users/aburrows/Documents/Security/Client Certificate/admissionsrocket.xyz-key.pem"

logging.basicConfig(level=logging.DEBUG)

def get_oauth_token():
    auth_header = f'Basic {base64.b64encode(f"{PCC_CLIENT_ID}:{PCC_CLIENT_SECRET}".encode()).decode()}'
    headers = {
        'authorization': auth_header,
        'content-type': 'application/x-www-form-urlencoded'
    }
    body = "grant_type=client_credentials"
    
    try:
        logging.debug(f"Requesting OAuth token with headers: {headers} and body: {body}")
        response = requests.post(TOKEN_ENDPOINT, headers=headers, data=body, cert=(CERT_FILE, KEY_FILE))
        response.raise_for_status()
        token_data = response.json()
        logging.debug(f"Received OAuth token: {token_data}")
        return token_data['access_token']
    except requests.RequestException as e:
        logging.error(f"Error obtaining OAuth token: {e}")
        logging.error(f"Response content: {e.response.content if e.response else 'No response'}")
        return None

def fetch_patient_data(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        "facId": 45
    }
    try:
        url = f"{PCC_API_BASE_ENDPOINT}/{ORGANIZATION_ID}/patients"
        logging.debug(f"Fetching patient data with URL: {url}, headers: {headers}, and params: {params}")
        response = requests.get(url, headers=headers, params=params, cert=(CERT_FILE, KEY_FILE))
        response.raise_for_status()
        patient_data = response.json()
        logging.debug(f"Received patient data: {patient_data}")
        return patient_data
    except requests.RequestException as e:
        logging.error(f"Error fetching patient data: {e}")
        if e.response:
            logging.error(f"Response content: {e.response.text}")
        else:
            logging.error("No response content available")
        return None
    
def patient_fetcher():
    token = get_oauth_token()
    if token:
        patient_data = fetch_patient_data(token)
        if patient_data:
            print("Patient data fetched successfully:")
            print(patient_data)
            return patient_data
        else:
            print("Failed to fetch patient data.")
    else:
        print("Failed to obtain OAuth token.")

def fetch_facilities(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        url = f"https://connect2.pointclickcare.com/api/public/preview1/orgs/{ORGANIZATION_ID}/facs"
        response = requests.get(url, headers=headers, cert=(CERT_FILE, KEY_FILE))
        response.raise_for_status()
        facilities_data = response.json()
        return facilities_data
    except requests.RequestException as e:
        logging.error(f"Error fetching facilities data: {e}")
        if e.response:
            logging.error(f"Response content: {e.response.text}")
        else:
            logging.error("No response content available")
        return None


def make_request(call_details, save_to_file):
    token = get_oauth_token()
    if not token:
        print("Failed to obtain OAuth token.")
        return

    # Construct URL using the constant ORGANIZATION_ID
    path = call_details['path'].replace("{orgUuid}", ORGANIZATION_ID)
    url = f"https://connect2.pointclickcare.com/api{path}"
    method = call_details['method']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    print(f'building {method} request to endpoint: {url}')

    # Collect parameters and filter out those with empty values
    params = {}
    for param in call_details['parameters']:
        if param['name'] == 'orgUuid':
            continue

        param_value = None
        # Always prompt the user for input
        while param['required'] and not param_value:
            param_value = input(f"Enter value for {param['name']} (required): ")
            if param['required'] and not param_value:
                print(f"{param['name']} is required. Please provide a value.")
        
        if not param['required']:
            param_value = input(f"Enter value for {param['name']} (optional): ")

        if param_value:
            params[param['name']] = param_value

    response = None
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, cert=(CERT_FILE, KEY_FILE))
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=params, cert=(CERT_FILE, KEY_FILE))
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=params, cert=(CERT_FILE, KEY_FILE))
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=params, cert=(CERT_FILE, KEY_FILE))
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, json=params, cert=(CERT_FILE, KEY_FILE))

        response.raise_for_status()

        if save_to_file:
            file_path = input("Enter file path to save response: ")
            with open(file_path, 'w') as file:
                file.write(response.text)
            return f"Response saved to {file_path}"
        else:
            return response.json()
    except requests.RequestException as e:
        logging.error(f"Error making API request: {e}")
        if response:
            logging.error(f"Response content: {response.text}")
        return f"Failed to make request: {e}"