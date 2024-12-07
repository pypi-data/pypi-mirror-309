import os
import requests
from Bio import Phylo
from ..kcat_prediction.dlkcat import download_file

def build_phylogenetic_tree(fasta_file_path, username, password, email,out_file):
    """
    Build a phylogenetic tree using the MAFFT algorithm via the Tree Build API.

    This function sends a POST request to the API with the provided FASTA file and user's email,
    along with authentication credentials. The API processes the FASTA file to construct a
    phylogenetic tree and returns a URL where the results can be viewed.

    Parameters:
    - fasta_file_path (str): Path to the FASTA file containing the sequences.
    - api_url (str): URL of the Tree Build API.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.
    - email (str): Email address for receiving the results.

    Returns:
    - str: URL where the results can be viewed if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    # Open the FASTA file in binary read mode
    with open(fasta_file_path, 'rb') as fasta_file:
        files = {
            'file': fasta_file
        }
        data = {
            'email': email
        }
        # Create an HTTP basic authentication object using the provided username and password
        auth = requests.auth.HTTPBasicAuth(username, password)
        api_url = 'https://www.mtc-lab.cn/km/api/tree_build_mafft/'

        # Send a POST request to the API with the file and data
        response = requests.post(api_url, files=files, data=data, auth=auth)

        # Check the response status code to determine if the request was successful
        if response.status_code == 200:
            # If successful, parse the JSON response and return the URL where the results can be viewed
            result = response.json()
            result_url = result['url']
            timestamp = result_url.split('/')[-1]
            out_file = f"{out_file}.csv"
            download_url=os.path.join('https://www.mtc-lab.cn/','static',f'foldseek/alntmscore/{timestamp }/result.csv')
            download_file(download_url,out_file)
            return result_url
        else:
            # If the request fails, print the error message and return None
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

# Usage example
if __name__ == "__main__":
    # Define the FASTA file path, API URL, authentication credentials, and email
    fasta_file_path = '/path/to/your/sequences.fasta'
    username = 'your_username'
    password = 'your_password'
    email = 'your_email@example.com'

    # Call the build_phylogenetic_tree function and store the result URL
    result_url = build_phylogenetic_tree(fasta_file_path,  username, password, email,"phylogenetic_tree")

    # Check if the tree construction was successful and print the result URL or an error message
    if result_url is not None:
        print(f"Results will be available at: {result_url}")
    else:
        print("Tree construction failed, please check your input and error messages.")
