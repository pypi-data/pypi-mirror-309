import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def analyze_plip(pdb_file_path, username, password,output_file_name=None):
    """
    Analyze protein-ligand interactions using the PLIP web service.
    
    This function submits a protein-ligand complex PDB file to the PLIP API for interaction analysis.
    It handles the API request, authentication, and downloading of results.

    Parameters:
    -----------
    pdb_file_path : str
        Path to the PDB file containing the protein-ligand complex structure
    username : str 
        Username for API authentication
    password : str
        Password for API authentication
    output_file_name : str, optional
        Custom name for the output zip file. If not provided, uses timestamp-based name

    Returns:
    --------
    str or None
        URL where analysis results can be downloaded if successful, None if request fails

    Notes:
    ------
    - Requires valid API authentication credentials
    - Input PDB file must exist and contain both protein and ligand structures
    - Results are downloaded as a zip file containing PLIP analysis outputs
    """
   
    api_url = 'https://www.mtc-lab.cn/docking_md/api/plip_analysis/'
    
    with open(pdb_file_path, 'rb') as pdb_file:
        files = {
            'pdb_file': pdb_file
        }
        auth = HTTPBasicAuth(username, password)
        
        response = requests.post(api_url, files=files, auth=auth)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                result_url = f"https://www.mtc-lab.cn{result['url']}"
                timestamp = result_url.split('/')[-1]
                web_host = "https://www.mtc-lab.cn"
                download_url = web_host+f"/static/docking_md/plip_analysis/{timestamp}/result.zip"
                if output_file_name is None:
                    output_file_name = timestamp+".zip"
                else:
                    output_file_name = output_file_name+".zip"
                    
                download_file(download_url,output_file_name)
                print(f"Analysis completed successfully!")
                return download_url
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
                return None
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

# Usage example
if __name__ == "__main__":
    pdb_file_path = '/path/to/your/complex.pdb'
    
    username = 'your_username'
    password = 'your_password'
    output_file_name = None
    result_url = analyze_plip(pdb_file_path, username, password,output_file_name)
    if result_url is not None:
        print(f"Results available at: {result_url}")
