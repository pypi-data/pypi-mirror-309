import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"File downloaded to: {local_filename}")

def autodock_vina(sdf_file_path, protein_file_path, position_file_path, email,  username, password,out_file=None):
    """
    Call the AutoDock Vina API to perform molecular docking.

    This function submits ligand (SDF), protein (PDB), and docking box position files to the AutoDock Vina API
    for molecular docking calculations. It handles the API request, authentication, and downloading of results.

    Parameters:
    - sdf_file_path (str): Path to the SDF file containing ligand structure
    - protein_file_path (str): Path to the PDB file containing protein structure  
    - position_file_path (str): Path to the text file containing docking box position parameters
    - email (str): Email address for receiving results
    - username (str): Username for API authentication
    - password (str): Password for API authentication
    - out_file (str, optional): Custom output filename for results zip file. If not provided,
                               defaults to 'result.zip'

    Returns:
    - str: URL where docking results can be downloaded if successful
    - None: If the request fails, prints error message and returns None

    Notes:
    - Requires valid API authentication credentials
    - Input files must exist and be properly formatted
    - Results are downloaded as a zip file containing docking outputs
    """
    
    
    web_host = "https://www.mtc-lab.cn"
    api_url = web_host + '/km/api/autodock_vina/'
    auth = HTTPBasicAuth(username, password)
    with open(sdf_file_path, 'rb') as sdf_file, open(protein_file_path, 'rb') as protein_file, open(position_file_path, 'rb') as position_file:
        files = {
            'ligand_file': sdf_file,
            'protein_file': protein_file,
            'position_file': position_file
        }
        data = {'email': email}
        try:
            print(f"Sending request to: {api_url}")
            response = requests.post(api_url, files=files, data=data, auth=auth)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            return None
    
    if response.status_code == 200:
        result = response.json()
        result_url = result.get('url')
        timestamp = result_url.split('/')[-1]
        download_url = f'{web_host}/static/docking_md/autodock_vina/{timestamp}/{timestamp}.zip'
        if out_file is not None:
            out_file = out_file+'.zip'
        else:
            out_file = 'result.zip'
        download_file(download_url,out_file)
        return download_url
    else:
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.text}")
        with open('error.html', 'w') as f:
            f.write(response.text)
        return None

# Usage example
if __name__ == "__main__":
    sdf_file_path = "/path/to/your/ligand.sdf"
    protein_file_path = "/path/to/your/protein.pdb"
    position_file_path = "/path/to/your/vina_box.txt"
    email = "your_email@example.com"
    username = 'your_username'
    password = 'your_password'
    web_host="https://www.mtc-lab.cn"
    out_file = "result.zip"

    result_url = autodock_vina(sdf_file_path, protein_file_path, position_file_path, email, username, password,out_file)
    if result_url:
        print(f"AutoDock Vina calculation completed. Results available at: {web_host}{result_url}")
    else:
        print("AutoDock Vina calculation failed.")
