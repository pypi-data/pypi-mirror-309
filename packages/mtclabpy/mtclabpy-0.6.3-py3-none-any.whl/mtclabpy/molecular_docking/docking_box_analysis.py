import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def analyze_box(pdb_file_path,  username, password, fold=1.0,vina_box_file_name=None,pocket_box_file_name=None):
    """
    Analyze protein binding pockets and generate docking box parameters.

    This function submits a protein structure file to analyze potential binding pockets and generate 
    appropriate docking box parameters for molecular docking. It handles API requests, authentication,
    and downloading of results files.

    Parameters:
    - pdb_file_path (str): Path to the PDB file containing protein structure
    - username (str): Username for API authentication 
    - password (str): Password for API authentication
    - fold (float, optional): Scaling factor for box size. Default is 1.0
    - vina_box_file_name (str, optional): Custom filename for Vina box parameters file.
                                         If not provided, defaults to 'vina_box.txt'
    - pocket_box_file_name (str, optional): Custom filename for PyMOL pocket visualization file.
                                           If not provided, defaults to 'pocket_box.pse'

    Returns:
    - str: URL where analysis results can be viewed if successful
    - None: If the request fails, prints error message and returns None

    Notes:
    - Requires valid API authentication credentials
    - Input PDB file must exist and be properly formatted
    - Downloads two result files:
        1. Vina box parameters file (.txt)
        2. PyMOL pocket visualization file (.pse)
    """
    
    
    api_url = 'https://www.mtc-lab.cn/docking_md/api/box_analysis/'
    with open(pdb_file_path, 'rb') as pdb_file:
        files = {
            'pdb_file': pdb_file
        }
        data = {
            'fold': fold
        }
        auth = HTTPBasicAuth(username, password)
        
        response = requests.post(api_url, files=files, data=data, auth=auth)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                result_url = f"https://www.mtc-lab.cn{result['url']}"
                timestamp = result_url.split('/')[-1]
                download_url_vina = f"https://www.mtc-lab.cn/static/docking_md/box_analysis/{timestamp}/vina_box.txt"
                download_url_pocket = f"https://www.mtc-lab.cn/static/docking_md/box_analysis/{timestamp}/pocket_box.pse"
                
                if vina_box_file_name is None:
                    vina_box_file_name = "vina_box.txt"
                else:
                    vina_box_file_name = vina_box_file_name+".txt"
                if pocket_box_file_name is None:
                    pocket_box_file_name = "pocket_box.pse"
                else:
                    pocket_box_file_name = pocket_box_file_name+".pse"
                
                download_file(download_url_vina, vina_box_file_name)
                download_file(download_url_pocket, pocket_box_file_name)
                print(f"Analysis completed successfully!")
                return result_url
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
                return None
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

# Usage example
if __name__ == "__main__":
    pdb_file_path = '/path/to/your/protein.pdb'
    username = 'your_username'
    password = 'your_password'
    vina_box_file_name = "vina_box.txt"
    pocket_box_file_name = "pocket_box.pse"

    result_url = analyze_box(pdb_file_path, username, password,vina_box_file_name=vina_box_file_name,pocket_box_file_name=pocket_box_file_name)
    if result_url is not None:
        print(f"Results available at: {result_url}")
