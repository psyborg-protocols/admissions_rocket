import pandas as pd

def fetch_patient_data():
    try:
        # Adjust the path to where your CSV file is located
        csv_file_path = "C:/Users/aburrows/Documents/Admissions_rocket_V0/admissions_app/static/test_data/patients.csv"
        df = pd.read_csv(csv_file_path)
        patients = df.to_dict('records')
        return patients
    except Exception as e:
        print(f"Error fetching patient data from CSV: {e}")
        return []
