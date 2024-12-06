import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def seq2mutation(seq_file_path,  username, password,outfile_name=None):
    """
    This function sends a POST request to the Sequence to Mutation API to generate all possible single-point mutations for a given sequence.

    Parameters:
    - seq_file_path (str): Path to the sequence file.
    - api_url (str): URL of the Sequence to Mutation API.
    - username (str): Username for basic authentication.
    - password (str): Password for basic authentication.

    Returns:
    - None: The function prints the result or error message directly.
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
        if result['success']:
            result_url = result['url']
            web_host = 'https://www.mtc-lab.cn'
            download_url = f"{web_host}{result_url}"
            if not outfile_name:
                outfile_name = result_url.split('/')[-1]
            else:
                outfile_name = outfile_name+'.txt'
            download_file(download_url, outfile_name)
            
            print(f"Mutation list generated. You can download it at: {result['url']}")
        else:
            print(f"Error: {result['error']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Usage example
if __name__ == "__main__":
    # API configuration
    
    username = 'your_username'
    password = 'your_password'
    
    # Task parameters
    seq_file_path = r'/path/to/your.fasta'
    outfile_name = 'your_output_file_name'
    # Execute the sequence to mutation generation task
    seq2mutation(seq_file_path,  username, password,outfile_name=outfile_name)
