import requests
from requests.auth import HTTPBasicAuth
import os
import pandas as pd

from ..kcat_prediction.dlkcat import download_file

def foldseek_cluster(pdb_files, email, username, password, out_file):
    """
    Perform protein structure clustering analysis using Foldseek Cluster API.

    Parameters:
    - pdb_files (list of str): List of PDB file paths or a single ZIP file path containing PDB files
    - email (str): Email address to receive results
    - username (str): API authentication username
    - password (str): API authentication password
    - out_file (str): Output file path (without extension, .tsv will be added automatically)

    Returns:
    - str: Result viewing URL if successful
    - None: If request fails, prints error message and returns None

    Features:
    1. Supports both single ZIP file and multiple PDB files upload
    2. Uses HTTP basic authentication for API access
    3. Automatically downloads clustering results as TSV file
    4. Returns URL for viewing results online
    """
    # Create an HTTP basic authentication object using the provided username and password
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/USalign/api/foldseek_cluster/'

    # Initialize the files dictionary to hold the PDB files or ZIP file
    files = {}

    # Check if a single ZIP file is provided
    if len(pdb_files) == 1 and pdb_files[0].endswith('.zip'):
        files['pdb_files'] = open(pdb_files[0], 'rb')
    else:
        # If multiple PDB files are provided, add each one to the files dictionary
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
        result_url = result['url']
        timestamp = result_url.split('/')[-1]
        out_file = f"{out_file}.tsv"
        download_url = os.path.join('https://www.mtc-lab.cn/', 'static', f'foldseek/cluster/{timestamp}/result_cluster.tsv')
        download_file(download_url, out_file)
        return result_url
    else:
        # If the request fails, print the error message and return None
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    # Define the API URL, authentication credentials, PDB files, and email
    
    username = 'your_username'
    password = 'your_password'
    pdb_files = ['/path/to/your/proteins.zip']  # or ['/path/to/protein1.pdb', '/path/to/protein2.pdb', ...]
    email = 'your_email@example.com'

    # Call the foldseek_cluster function and store the result URL
    result_url = foldseek_cluster(pdb_files, email, username, password)

    # Check if the clustering was successful and print the result URL or an error message
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
