import requests
from requests.auth import HTTPBasicAuth
import os

def download_file(url, local_filename):
    """
    Download a file from a given URL and save it to the specified local filename.

    Parameters:
    - url (str): The URL of the file to download.
    - local_filename (str): The local filename to save the downloaded file.

    Returns:
    - None
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"File downloaded to: {local_filename}")
def autodock_ff(ligand_file_path, protein_file_path, email, username, password,out_file=None):
    """
    Call the AutoDock FF API to perform molecular docking.

    This function checks if the ligand and protein files exist, reads their contents, and sends a POST request
    to the specified API endpoint with the file contents, email, and user authentication. If the request is successful,
    it prints the success message and returns the URL where the results can be accessed. If there are any errors,
    it prints the error messages.

    Parameters:
    - ligand_file_path (str): The path to the SDF file containing the ligand structure.
    - protein_file_path (str): The path to the PDB file containing the protein structure.
    - email (str): Email address for receiving the results.
    - api_url (str): The URL of the AutoDock FF API endpoint.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.

    Returns:
    - str: The URL where the results can be accessed if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    api_url = 'https://www.mtc-lab.cn/km/api/AutoDock_FF/'
    web_host = 'https://www.mtc-lab.cn'
    
    # Check if files exist
    if not os.path.exists(ligand_file_path):
        print(f"Error: Ligand file not found at {ligand_file_path}")
        return
    if not os.path.exists(protein_file_path):
        print(f"Error: Protein file not found at {protein_file_path}")
        return

    # Read file contents
    with open(ligand_file_path, 'rb') as ligand_file:
        ligand_content = ligand_file.read()
    with open(protein_file_path, 'rb') as protein_file:
        protein_content = protein_file.read()

    files = {
        'ligand_file': ('ligand.sdf', ligand_content, 'chemical/x-sdf'),
        'protein_file': ('protein.pdb', protein_content, 'chemical/x-pdb')
    }
    data = {
        'email': email
    }
    auth = HTTPBasicAuth(username, password)
    
    try:
        response = requests.post(api_url, files=files, data=data, auth=auth)
        response.raise_for_status()
        
        if response.status_code == 200:
            json_response = response.json()
            print("Success:", json_response)
            result_url = json_response['url']
            timestamp = result_url.split('/')[-1]
            download_url = web_host+f"/static/docking_md/autodock_ff/{timestamp}/{timestamp}.zip"
            if out_file is not None:
                out_file = out_file+'.zip'
            else:
                out_file="result.zip"
            download_file(download_url,out_file)

            return download_url
        else:
            print(f"Error: {response.status_code}")
            print("Response content:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'response'):
            print(f"Error response: {e.response.text}")

# Usage example
if __name__ == "__main__":
    ligand_file_path = '/path/to/your/ligand.sdf'
    protein_file_path = '/path/to/your/protein.pdb'
    email = 'your_email@example.com'
    username = 'your_username'
    password = 'your_password'
    out_file = "result.zip"
    result_url = autodock_ff(ligand_file_path, protein_file_path, email, username, password,out_file)
    if result_url:
        print(f"Result URL: {result_url}")
