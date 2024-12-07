import requests
from requests.auth import HTTPBasicAuth
import os

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def pocket_detector(pdb_file, email, username, password,output_file_name=None):
    """
    Call the FPocket API to detect protein pockets.

    This function submits a protein structure file to detect potential binding pockets using FPocket.
    It handles the API request, authentication, and downloading of results.

    Parameters:
    -----------
    pdb_file : str
        Path to the PDB file containing protein structure
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
        URL where pocket detection results can be downloaded if successful, None if request fails

    Notes:
    ------
    - Requires valid API authentication credentials
    - Input PDB file must exist and be properly formatted
    - Results are downloaded as a zip file containing FPocket outputs
    """

    api_url = 'https://www.mtc-lab.cn/USalign/api/pocket_detector/'
    auth = HTTPBasicAuth(username, password)

    files = {
        'pdb_file': open(pdb_file, 'rb'),
    }

    data = {
        'email': email,
    }

    response = requests.post(api_url, files=files, data=data, auth=auth)

    files['pdb_file'].close()

    if response.status_code == 200:
        result = response.json()
        result_url = f"https://www.mtc-lab.cn{result['url']}"
        timestamp = result_url.split('/')[-1]
        download_url = f"https://www.mtc-lab.cn/static/fpocket/{timestamp}/{timestamp}.zip"
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
    pdb_file = '/path/to/your/protein.pdb'
    email = 'your_email@example.com'
    output_file_name = 'your_output_file_name.zip'

    result_url = pocket_detector(pdb_file, email, username, password,output_file_name)
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
