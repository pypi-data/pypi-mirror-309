# This module provides functionality to convert distance matrices to phylogenetic trees
# using the Matrix to Tree API service from MTC-Lab
import os
import numpy as np
import pandas as pd
import requests
from Bio import Phylo
from ..kcat_prediction.dlkcat import download_file

def matrix2tree(excel_file, email, username, password, out_file):
    """
    Convert a distance matrix from an Excel file to a phylogenetic tree using the Matrix to Tree API.

    This function sends a POST request to the API with the provided Excel file and user's email,
    along with authentication credentials. The API processes the distance matrix and generates a
    phylogenetic tree, returning a URL where the results can be viewed and downloads the tree file.

    Parameters:
    - excel_file (str): Path to the Excel file containing the distance matrix.
    - email (str): Email address for receiving the results.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.
    - out_file (str): Base name for the output tree file (will be appended with '.result.treefile')

    Returns:
    - str: URL where the results can be viewed if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    # Create an HTTP basic authentication object for API access
    auth = requests.auth.HTTPBasicAuth(username, password)

    # Open and prepare the Excel file for upload
    files = {'file': open(excel_file, 'rb')}

    # Prepare the request data including user's email
    data = {
        'email': email,
    }
    # Define the API endpoint URL
    api_url = 'https://www.mtc-lab.cn/km/api/matrix2tree/'

    # Send POST request to the API with the file, data, and authentication
    response = requests.post(api_url, files=files, data=data, auth=auth)

    # Ensure proper file cleanup
    files['file'].close()

    # Process the API response
    if response.status_code == 200:
        # Extract result information from successful response
        result = response.json()
        result_url = result['url']
        
        # Extract timestamp from URL for downloading the result file
        timestamp = result_url.split('/')[-1]
        
        # Construct output filename and download URL
        out_file = f"{out_file}.result.treefile"
        download_url = os.path.join('https://www.mtc-lab.cn/', 'static', 'matrix2tree', 
                                  str(timestamp), 'result.treefile')
        
        # Download the resulting tree file
        download_file(download_url, out_file)
        return result_url
    else:
        # Handle API request failures
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example usage demonstration
if __name__ == "__main__":
    # Example configuration - replace with actual values
    username = 'your_username'
    password = 'your_password'
    excel_file = '/path/to/your/matrix.xlsx'
    email = 'your_email@example.com'
    out_file = 'your_out_file'
    
    # Attempt to generate the tree and get results
    result_url = matrix2tree(excel_file, email, username, password, out_file)

    # Display the results or error message
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
