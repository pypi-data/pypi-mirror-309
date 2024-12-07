import requests
from requests.auth import HTTPBasicAuth
import os

def download_file(url, local_filename):
    """
    Download a file from a URL and save it to a local file.
    
    Parameters:
    - url (str): URL of the file to download
    - local_filename (str): Path where to save the downloaded file
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def generate_mutations(seq_file_path, username, password, outfile_name=None):
    """
    Generate all possible single-point mutations for a given protein sequence.

    Parameters:
    - seq_file_path (str): Path to the sequence file in FASTA format
    - username (str): Username for API authentication
    - password (str): Password for API authentication
    - outfile_name (str, optional): Name for the output file (without extension).
                                  If not provided, will use the original filename.

    Returns:
    - str: URL to the result if successful, None otherwise
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/mutation/api/seq2mutation/'
    
    # Open the sequence file in binary mode
    with open(seq_file_path, 'rb') as seq_file:
        files = {'seq_file': seq_file}
        
        # Send the POST request
        response = requests.post(api_url, files=files, auth=auth)
    
    # Handle the response
    if response.status_code == 200:
        result = response.json()
        if not result.get('success', True):  # Check for API-level errors
            print(f"API Error: {result.get('error', 'Unknown error')}")
            return None
            
        result_url = result['url']
        web_host = 'https://www.mtc-lab.cn'
        download_url = f"{web_host}{result_url}"
        
        try:
            if not outfile_name:
                outfile_name = os.path.splitext(os.path.basename(seq_file_path))[0]
            save_name = f"{outfile_name}_mutations.txt"
            
            download_file(download_url, save_name)
            print(f"Downloaded mutation list to: {save_name}")
            return result_url
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    username = 'your_username'
    password = 'your_password'
    seq_file_path = r'/path/to/your.fasta'
    outfile_name = 'my_protein'
    
    result_url = generate_mutations(seq_file_path, username, password, outfile_name)
    if result_url:
        print(f"You can check the results at: {result_url}")
    else:
        print("Mutation generation failed, please check the error messages above.")
