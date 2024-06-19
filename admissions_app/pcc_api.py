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

#Gets an Oauth token to access PCC API
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

#make_request method: takes call details and makes a request to PCC API
#params:a dictionary with the details of the call to be made
#   {
#   'path':'/public/preview1/orgs/{orgUuid}/patients'
#   'method': 'GET'
#   'path_params': {'orgUuid': '7daf45ae-1982-4b95-9df8-46a067df0de7',}
#   'call_params': {'facId': 12,}
#   }


def make_request(call_details):
    token = get_oauth_token()
    if not token:
        print("Failed to obtain OAuth token.")
        return

    # Construct URL using the path params
    for param in call_details['path_params']:    
        path = call_details['path'].replace(f'{{{param}}}', call_details['path_params'][param])
    url = f"https://connect2.pointclickcare.com/api{path}"
    method = call_details['method']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    params = call_details['call_params']

    print(f'building {method} request to endpoint: {url}')

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

        return response.json()

    except requests.RequestException as e:
        logging.error(f"Error making API request: {e}")
        if response:
            logging.error(f"Response content: {response.text}")
        return f"Failed to make request: {e}"