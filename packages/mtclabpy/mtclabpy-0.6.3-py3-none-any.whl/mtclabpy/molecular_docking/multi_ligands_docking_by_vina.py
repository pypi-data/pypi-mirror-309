import requests
from requests.auth import HTTPBasicAuth
import os

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def autodock_vina_one_protein_multi_ligands(protein_file, ligand_files, txt_file, email, username, password,output_file_name=None):
    """
    Call the AutoDock Vina API to perform molecular docking with one protein and multiple ligands.

    This function submits one protein structure file and multiple ligand files along with docking box parameters
    to perform batch molecular docking calculations. It handles the API request, authentication, and downloading
    of results.

    Parameters:
    - protein_file (str): Path to the PDB file containing protein structure
    - ligand_files (list): List of paths to SDF files containing ligand structures
    - txt_file (str): Path to text file containing docking box position parameters
    - email (str): Email address for receiving results
    - username (str): Username for API authentication
    - password (str): Password for API authentication 
    - output_file_name (str, optional): Custom output filename for results zip file. If not provided,
                                      defaults to timestamp-based name

    Returns:
    - str: URL where docking results can be downloaded if successful
    - None: If the request fails, prints error message and returns None

    Notes:
    - Requires valid API authentication credentials
    - Input files must exist and be properly formatted
    - Results are downloaded as a zip file containing docking outputs for all ligands
    """
    
    api_url = 'https://www.mtc-lab.cn/km/api/autodock_vina_one_protein_multi_ligands/'
    auth = HTTPBasicAuth(username, password)

    files = {
        'protein_file': open(protein_file, 'rb'),
        'txt_file': open(txt_file, 'rb'),
    }
    for i, ligand_file in enumerate(ligand_files):
        files[f'ligand_file_{i}'] = open(ligand_file, 'rb')

    data = {
        'email': email,
    }

    response = requests.post(api_url, files=files, data=data, auth=auth)

    for file in files.values():
        file.close()

    if response.status_code == 200:
        result = response.json()
        result_url = result['url']
        timestamp = result_url.split('/')[-1]
        web_host = "https://www.mtc-lab.cn"
        download_url = web_host+f"/static/docking_md/autodock_vina_one_protein_multi_ligands/{timestamp}/{timestamp}.zip"
        if output_file_name is None:
            output_file_name = timestamp+".zip"
        else:
            output_file_name = output_file_name+".zip"
            
        download_file(download_url,output_file_name)
        
        return download_url
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    
    username = 'your_username'
    password = 'your_password'
    protein_file = '/path/to/your/protein.pdb'
    ligand_files = [
        '/path/to/your/ligand1.sdf',
        '/path/to/your/ligand2.sdf'
    ]
    txt_file = '/path/to/your/vina_box.txt'
    email = 'your_email@example.com'

    result_url = autodock_vina_one_protein_multi_ligands(protein_file, ligand_files, txt_file, email, username, password)
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
