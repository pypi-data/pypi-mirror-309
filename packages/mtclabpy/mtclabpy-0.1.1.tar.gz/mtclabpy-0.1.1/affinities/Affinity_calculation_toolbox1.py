import requests
from requests.auth import HTTPBasicAuth

def calculate_affability(pdb_file_path, mol2_file_path, api_url, username, password):
    """
    Calculate the affinity (pKd) using the provided PDB and MOL2 files.

    This function sends a POST request to a specified API with the given PDB and MOL2 files to calculate the affinity index (pKd).

    Parameters:
    - pdb_file_path (str): Path to the PDB file.
    - mol2_file_path (str): Path to the MOL2 file.
    - api_url (str): URL of the API used for calculating the affinity.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.

    Returns:
    - float: The calculated affinity index (pKd) if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    # Open the PDB and MOL2 files to be sent to the API
    with open(pdb_file_path, 'rb') as pdb_file, open(mol2_file_path, 'rb') as mol2_file:
        # Create a dictionary to store the files to be sent
        files = {
            'pdb_file': pdb_file,
            'mol2_file': mol2_file
        }
        # Create an HTTP basic authentication object using the provided username and password
        auth = HTTPBasicAuth(username, password)

        # Send a POST request to the API with the files and authentication information
        response = requests.post(api_url, files=files, auth=auth)

        # Check the response status code to determine if the request was successful
        if response.status_code == 200:
            # If successful, parse the JSON response and return the pKd value
            result = response.json()
            return result['pKd']
        else:
            # If the request fails, print the error message and return None
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

# Usage example
if __name__ == "__main__":
    pdb_file_path = '/path/to/your/protein.pdb'
    mol2_file_path = '/path/to/your/ligand.mol2'
    api_url = 'https://www.mtc-lab.cn/docking_md/api/affability_calc/'
    username = 'your_username'
    password = 'your_password'

    pkd = calculate_affability(pdb_file_path, mol2_file_path, api_url, username, password)
    if pkd is not None:
        print(f"Calculated pKd: {pkd}")
