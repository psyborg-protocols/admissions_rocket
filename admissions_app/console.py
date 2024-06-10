import json

def load_api_data():
    with open('C:\\Users\\aburrows\\Documents\\Admissions_rocket_V0\\admissions_app\\static\\api_data\\openapi.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def list_valid_calls(api_data, search_term):
    calls = []
    for path, methods in api_data['paths'].items():
        for method, details in methods.items():
            if search_term.lower() in path.lower():
                path_parameters = []
                other_parameters = []
                for param in details.get('parameters', []):
                    param_info = {'name': param['name'], 'required': param.get('required', False)}
                    if param['in'] == 'path':
                        path_parameters.append(param_info)
                    else:
                        other_parameters.append(param_info)
                
                calls.append({
                    'method': method.upper(),
                    'description': details.get('description', 'No description'),
                    'path': path,
                    'path_parameters': path_parameters,
                    'parameters': other_parameters
                })
    return calls

def prompt_user(api_data):
    search_term = input("Enter a search term: ")
    valid_calls = list_valid_calls(api_data, search_term)
    if not valid_calls:
        print("No valid API calls found for the search term.")
        return None, False
    
    while True:
        for i, call in enumerate(valid_calls, 1):
            path_params = ', '.join([f"{p['name']} (required)" if p['required'] else p['name'] for p in call['path_parameters']])
            params = ', '.join([f"{p['name']} (required)" if p['required'] else p['name'] for p in call['parameters']])
            print(f"{i}) {call['method']} {call['description']} - path: {call['path']} - path params: {path_params} - params: {params}")
        try:
            choice = int(input("Select an API call to make (number): ")) - 1
            if 0 <= choice < len(valid_calls):
                break
            else:
                print("Invalid choice. Please enter a number corresponding to one of the valid API calls.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    save_to_file = input("Save results to file? (yes/no): ").lower() == 'yes'
    return valid_calls[choice], save_to_file


def run_console():
    api_data = load_api_data()
    while True:
        selected_call, save_to_file = prompt_user(api_data)
        if selected_call is None:
            continue
        from admissions_app.pcc_api import make_request
        response = make_request(selected_call, save_to_file)
        if not save_to_file:
            print("Response:", response)
        if input("Do you want to make another request? (yes/no): ").lower() != 'yes':
            break

if __name__ == "__main__":
    run_console()
