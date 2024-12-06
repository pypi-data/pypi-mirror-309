import requests
from requests.auth import HTTPBasicAuth
import os

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def caverdock(receptor_file, ligand_file, tunel_file, email, username, password,output_file_name=None):
    """
    Call the CaverDock API to perform tunnel docking calculations.

    This function submits a receptor structure, ligand structure and tunnel file to perform 
    tunnel docking using CaverDock. It handles the API request, authentication, and downloading
    of results.

    Parameters:
    -----------
    receptor_file : str
        Path to the PDB file containing receptor structure
    ligand_file : str
        Path to the PDB file containing ligand structure 
    tunel_file : str
        Path to the PDB file containing tunnel information
    email : str
        Email address for receiving results
    username : str
        Username for API authentication
    password : str
        Password for API authentication
    output_file_name : str, optional
        Custom output filename for results zip file. If not provided,
        defaults to timestamp-based name

    Returns:
    --------
    str or None
        URL where docking results can be downloaded if successful, None if request fails

    Notes:
    ------
    - Requires valid API authentication credentials
    - Input files must exist and be properly formatted
    - Results are downloaded as a zip file containing CaverDock outputs
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/docking_md/api/caverdock/'

    files = {
        'receptor_file': open(receptor_file, 'rb'),
        'ligand_file': open(ligand_file, 'rb'),
        'tunel_file': open(tunel_file, 'rb'),
    }

    data = {
        'email': email,
    }

    response = requests.post(api_url, files=files, data=data, auth=auth)

    for file in files.values():
        file.close()

    if response.status_code == 200:
        result = response.json()
        result_url = f"https://www.mtc-lab.cn{result['url']}"
        timestamp = result_url.split('/')[-1]
        download_url = f"https://www.mtc-lab.cn/static/docking_md/caverdock/{timestamp}/{timestamp}.zip"
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
    receptor_file = '/path/to/your/receptor.pdb'
    ligand_file = '/path/to/your/ligand.pdb'
    tunel_file = '/path/to/your/tunnel.pdb'
    email = 'your_email@example.com'

    result_url = caverdock(receptor_file, ligand_file, tunel_file, email, username, password)
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
