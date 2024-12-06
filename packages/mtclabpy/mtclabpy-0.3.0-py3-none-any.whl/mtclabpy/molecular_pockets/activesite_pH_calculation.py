
import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def predict_activesite_pH(fasta_file_path, pdb_files_paths, email, username, password,output_file_name=None):
    """
    Predict active site pH by sending files to a web service and downloading results.
    
    Args:
        fasta_file_path (str): Path to the FASTA file containing protein sequences
        pdb_files_paths (list): List of paths to PDB structure files
        email (str): User's email address for receiving results
        username (str): Username for API authentication
        password (str): Password for API authentication
        output_file_name (str, optional): Custom name for the output ZIP file. 
                                        If None, uses timestamp as filename.
    
    Returns:
        str or None: Download URL of the results if successful, None if failed
    
    The function:
    1. Sends FASTA and PDB files to the web service
    2. Authenticates using provided credentials
    3. Downloads results as a ZIP file if successful
    4. Returns the download URL or None if any errors occur
    """

    web_host = "https://www.mtc-lab.cn"
    api_url = web_host + '/km/api/activesite_pH/'
    auth = HTTPBasicAuth(username, password)
    
    # Open all files
    files = {'fast-file': open(fasta_file_path, 'rb')}
    for pdb_path in pdb_files_paths:
        files['pdb-files'] = open(pdb_path, 'rb')
    
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
    finally:
        # Close all opened files
        for f in files.values():
            f.close()
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            result_url = result.get('url')
            timestamp = result_url.split('/')[-1]
            web_host = "https://www.mtc-lab.cn"
            download_url = f'{web_host}/static/km_kcat/activesite_pH/{timestamp}/result.zip'
            if output_file_name is None:
                output_file_name = timestamp + ".zip"
            else:
                output_file_name = output_file_name + ".zip"
            download_file(download_url,output_file_name)
            return download_url
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return None
    else:
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

# Usage example
if __name__ == "__main__":
    fasta_file = "/path/to/your/sequences.fasta"
    pdb_files = [
        "/path/to/your/structure1.pdb",
        "/path/to/your/structure2.pdb"
    ]
    email = "your_email@example.com"
    username = 'your_username'
    password = 'your_password'
    output_file_name = 'your_output_file_name.zip'
    result_url = predict_activesite_pH(fasta_file, pdb_files, email, username, password,output_file_name)
    print(result_url)

