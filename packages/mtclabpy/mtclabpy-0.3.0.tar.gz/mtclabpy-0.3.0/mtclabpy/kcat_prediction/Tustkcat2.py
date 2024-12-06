import requests
from requests.auth import HTTPBasicAuth
import os

def Tust2_kcat(pdb_file_path, mol2_file_path, username, password):
    """
    Predict kcat values using protein PDB and ligand MOL2 files via API
    
    Parameters:
        pdb_file_path (str): Path to the protein structure PDB file
        mol2_file_path (str): Path to the ligand structure MOL2 file  
        username (str): API authentication username
        password (str): API authentication password
        
    Functions:
        1. Validates input file paths exist
        2. Reads PDB and MOL2 file contents
        3. Submits files to prediction API with authentication
        4. Retrieves and returns predicted kcat value
        
    Returns:
        float: Predicted kcat value if successful
        None: If API call fails or files not found
        
    Notes:
        - Requires valid API authentication credentials
        - Input files must be properly formatted PDB and MOL2
        - PDB file should contain protein structure
        - MOL2 file should contain ligand structure
    """

    
    api_url = 'https://www.mtc-lab.cn/km/api/predict-kcat/'
    # Check if files exist
    if not os.path.exists(pdb_file_path):
        print(f"Error: PDB file not found at {pdb_file_path}")
        return
    if not os.path.exists(mol2_file_path):
        print(f"Error: MOL2 file not found at {mol2_file_path}")
        return

    # Read file contents
    with open(pdb_file_path, 'rb') as pdb_file:
        pdb_content = pdb_file.read()
    with open(mol2_file_path, 'rb') as mol2_file:
        mol2_content = mol2_file.read()

    files = {
        'pdb_file': ('protein.pdb', pdb_content, 'chemical/x-pdb'),
        'mol2_file': ('ligand.mol2', mol2_content, 'chemical/x-mol2')
    }

    auth = HTTPBasicAuth(username, password)

    try:
        response = requests.post(api_url, files=files, auth=auth)
        response.raise_for_status()

        if response.status_code == 200:
            json_response = response.json()
            print("Success:", json_response)
            return json_response['kcat']
        else:
            print(f"Error: {response.status_code}")
            print("Response content:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'response'):
            print(f"Error response: {e.response.text}")

# Usage example
if __name__ == "__main__":
    pdb_file_path = '/path/to/your/protein.pdb'
    mol2_file_path = '/path/to/your/ligand.mol2'
    
    username = 'your_username'
    password = 'your_password'

    kcat_value = Tust2_kcat(pdb_file_path, mol2_file_path, username, password)
    if kcat_value:
        print(f"Predicted kcat value: {kcat_value}")
