import requests
from requests.auth import HTTPBasicAuth
import os

def foldseek_msa(pdb_files, email, username, password,out_file):
    """
    Perform Multiple Sequence Alignment (MSA) on protein structures using the Foldseek MSA API.

    This function sends a POST request to the API with the provided PDB files or a ZIP file containing PDB files,
    along with the user's email and authentication credentials. The API processes the protein structures and
    returns a URL where the results can be viewed.

    Parameters:
    - pdb_files (list of str): List of paths to the PDB files or a single path to a ZIP file containing PDB files.
    - email (str): Email address for receiving the results.
    - api_url (str): URL of the Foldseek MSA API.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.

    Returns:
    - str: URL where the results can be viewed if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    # Create an HTTP basic authentication object using the provided username and password
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/USalign/api/foldseek_msa/'

    # Initialize the files dictionary to hold the PDB files or ZIP file
    files = {}

    # Check if a single ZIP file is provided
    if len(pdb_files) == 1 and pdb_files[0].endswith('.zip'):
        files['pdb_files'] = open(pdb_files[0], 'rb')
    else:
        # If multiple PDB files are provided, add each one to the files dictionary
        for i, pdb_file in enumerate(pdb_files):
            files[f'pdb_file_{i}'] = open(pdb_file, 'rb')

    # Prepare the data to be sent to the API
    data = {
        'email': email,
    }

    # Send a POST request to the API with the files and data
    response = requests.post(api_url, files=files, data=data, auth=auth)

    # Close all opened files
    for file in files.values():
        file.close()

    # Check the response status code to determine if the request was successful
    if response.status_code == 200:
        # If successful, parse the JSON response and return the URL where the results can be viewed
        result = response.json()
        result_url = result['url']
        timestamp = result_url.split('/')[-1]
        out_file = f"{out_file}.zip"
        download_url = os.path.join('https://www.mtc-lab.cn/', 'static', f'foldseek/msa/{timestamp}/msa.zip')
        download_file(download_url, out_file)
        return result_url
    else:
        # If the request fails, print the error message and return None
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def download_file(url, output_file):
    """
    Download a file from a given URL and save it to the specified output file.
    
    Parameters:
    - url (str): The URL to download the file from
    - output_file (str): The path where the downloaded file should be saved
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"File successfully downloaded to {output_file}")
    else:
        print(f"Failed to download file: {response.status_code}")

# Usage example
if __name__ == "__main__":
    # Define the API URL, authentication credentials, PDB files, and email
    username = 'your_username'
    password = 'your_password'
    pdb_files = ['/path/to/your/proteins.zip']  # or ['/path/to/protein1.pdb', '/path/to/protein2.pdb', ...]
    email = 'your_email@example.com'
    out_file = 'your_out_file'
    # Call the foldseek_msa function and store the result URL
    result_url = foldseek_msa(pdb_files, email, username, password,out_file)

    # Check if the MSA was successful and print the result URL or an error message
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
