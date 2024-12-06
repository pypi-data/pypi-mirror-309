import requests
from requests.auth import HTTPBasicAuth
import os

def calculation1(pdb_files, email, api_url, username, password):
    """
    Perform USalign calculations on protein structures using the USalign Calculation1 API.

    This function sends a POST request to the API with the provided PDB files or a ZIP file containing PDB files,
    along with the user's email and authentication credentials. The API performs the USalign calculation and returns
    a URL where the results can be viewed.

    Parameters:
    - pdb_files (list of str): List of paths to the PDB files or a single path to a ZIP file containing PDB files.
    - email (str): Email address for receiving the results.
    - api_url (str): URL of the USalign Calculation1 API.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.

    Returns:
    - str: URL where the results can be viewed if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    # Create an HTTP basic authentication object using the provided username and password
    auth = HTTPBasicAuth(username, password)

    # Prepare the files to be sent to the API
    files = {}
    if len(pdb_files) == 1 and pdb_files[0].endswith('.zip'):
        # If a single ZIP file is provided, open it and add to the files dictionary
        files['pdb_files'] = open(pdb_files[0], 'rb')
    else:
        # If multiple PDB files are provided, open each one and add to the files dictionary
        for i, pdb_file in enumerate(pdb_files):
            files[f'pdb_file_{i}'] = open(pdb_file, 'rb')

    # Prepare the data to be sent to the API
    data = {
        'email': email,
    }

    # Send a POST request to the API with the files and data
    response = requests.post(api_url, files=files, data=data, auth=auth)

    # Close all opened files
    for file in files.values():
        file.close()

    # Check the response status code to determine if the request was successful
    if response.status_code == 200:
        # If successful, parse the JSON response and return the URL where the results can be viewed
        result = response.json()
        return result['url']
    else:
        # If the request fails, print the error message and return None
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    api_url = 'https://www.mtc-lab.cn/USalign/api/calculation1/'
    username = 'your_username'
    password = 'your_password'
    pdb_files = ['/path/to/your/protein.pdb']  # or ['/path/to/your/proteins.zip']
    email = 'your_email@example.com'

    result_url = calculation1(pdb_files, email, api_url, username, password)
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
