import requests
from requests.auth import HTTPBasicAuth
import os
from ..kcat_prediction.dlkcat import download_file

def foldseek_alntmscore(pdb_files, email, username, password, out_file):
    """
    Perform structural alignment and TM-score calculation between protein structures using Foldseek AlnTmscore API.
    
    This function provides a convenient interface to the Foldseek AlnTmscore web service for comparing
    protein 3D structures. It supports both single PDB file comparisons and batch processing through ZIP files.
    The results include structural alignment scores and TM-scores indicating structural similarity.

    Parameters:
    -----------
    pdb_files : list of str
        List containing either:
        - Multiple paths to individual PDB files for comparison
        - Single path to a ZIP file containing multiple PDB files
    email : str
        User's email address where the results notification will be sent
    username : str
        Username for API authentication
    password : str
        Password for API authentication
    out_file : str
        Base name for the output file (will be appended with .csv)

    Returns:
    --------
    str or None
        - If successful: Returns the URL where results can be viewed online
        - If failed: Returns None and prints error message

    Notes:
    ------
    - The API endpoint is hosted at mtc-lab.cn
    - Results are provided in CSV format
    - Authentication is required for API access
    """
    # Set up authentication for the API request
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/USalign/api/foldseek_alntmscore/'

    # Initialize dictionary for file uploads
    files = {}

    # Handle file upload preparation based on input type
    if len(pdb_files) == 1 and pdb_files[0].endswith('.zip'):
        # Case: Single ZIP file containing multiple PDB files
        files['pdb_files'] = open(pdb_files[0], 'rb')
    else:
        # Case: Multiple individual PDB files
        for i, pdb_file in enumerate(pdb_files):
            files[f'pdb_file_{i}'] = open(pdb_file, 'rb')

    # Prepare request data
    data = {
        'email': email,
    }

    # Send POST request to the API
    response = requests.post(api_url, files=files, data=data, auth=auth)

    # Clean up: close all opened files
    for file in files.values():
        file.close()

    # Process API response
    if response.status_code == 200:
        # Extract result information from successful response
        result = response.json()
        result_url = result['url']
        
        # Extract timestamp from URL for downloading results
        timestamp = result_url.split('/')[-1]
        out_file = f"{out_file}.csv"
        
        # Construct download URL and fetch results file
        download_url = os.path.join('https://www.mtc-lab.cn/', 
                                  'static', 
                                  f'foldseek/alntmscore/{timestamp}/result.csv')
        download_file(download_url, out_file)
        return result_url
    else:
        # Handle failed request
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example usage demonstration
if __name__ == "__main__":
    # Example configuration
    username = 'your_username'
    password = 'your_password'
    pdb_files = ['/path/to/your/proteins.zip']  # or ['/path/to/protein1.pdb', '/path/to/protein2.pdb', ...]
    email = 'your_email@example.com'
    out_file = 'your_out_file'

    # Execute structural comparison
    result_url = foldseek_alntmscore(pdb_files, email, username, password, out_file)

    # Display results or error message
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
