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

def pssm_generate(fasta_file, username, password, email, outfile_name=None):
    """
    Generate PSSM (Position-Specific Scoring Matrix) for a protein sequence.
    
    Parameters:
    - fasta_file (str): Path to the FASTA file containing the protein sequence
    - username (str): Username for API authentication
    - password (str): Password for API authentication
    - email (str): Email address to receive results
    - outfile_name (str, optional): Base name for output files (without extension).
                                  If not provided, will use the original filename.
    
    Returns:
    - str: URL to access the results if successful, None otherwise
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/mutation/api/pssm_generation/'
    
    # Prepare the file to upload
    with open(fasta_file, 'rb') as f:
        files = {'fasta_file': f}
        data = {'email': email}
        
        # Send the request
        response = requests.post(api_url, files=files, data=data, auth=auth)
    
    # Handle the response
    if response.status_code == 200:
        result = response.json()
        if not result.get('success', True):  # Check for API-level errors
            print(f"API Error: {result.get('error', 'Unknown error')}")
            return None
            
        result_url = result['url']
        timestamp = result_url.split('/')[-1]
        
        # Download the result files
        base_url = "https://www.mtc-lab.cn/static/mutation/pssm/"
        files_to_download = [
            "pssm.txt",
            "pssm_info.csv"
        ]
        
        for file_name in files_to_download:
            download_url = f"{base_url}{timestamp}/{file_name}"
            try:
                if not outfile_name:
                    outfile_name = os.path.splitext(os.path.basename(fasta_file))[0]
                save_name = f"{outfile_name}_{file_name}"
                download_file(download_url, save_name)
                print(f"Downloaded {file_name} to {save_name}")
            except Exception as e:
                print(f"Error downloading {file_name}: {str(e)}")
        return result_url
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    username = 'your_username'
    password = 'your_password'
    fasta_file = r'/path/to/your.fasta'
    email = 'your_email@example.com'
    outfile_name = 'my_pssm'
    
    result_url = pssm_generate(fasta_file, username, password, email, outfile_name)
    if result_url:
        print(f"PSSM generation started. Results will be sent to {email}")
        print(f"You can check the results at: {result_url}")
    else:
        print("PSSM generation failed, please check the error messages above.")
