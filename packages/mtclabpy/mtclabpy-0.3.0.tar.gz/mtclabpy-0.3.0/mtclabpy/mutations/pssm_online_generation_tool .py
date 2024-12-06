import requests
from requests.auth import HTTPBasicAuth

def pssm_generation(sequence_file, email, username, password):
    """
    This function sends a POST request to the PSSM Generation API to generate a Position-Specific Scoring Matrix (PSSM) from a sequence file.

    Parameters:
    - sequence_file (str): Path to the sequence file (FASTA format).
    - email (str): Email address for receiving the results.
    - api_url (str): URL of the PSSM Generation API.
    - username (str): Username for basic authentication.
    - password (str): Password for basic authentication.

    Returns:
    - str: URL to the generated PSSM file if the request is successful, otherwise None.
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/mutation/api/pssm_generation/'
    
    # Prepare the file to upload
    files = {
        'sequence-file': open(sequence_file, 'rb')
    }
    
    # Prepare the request data
    data = {
        'email': email,
    }
    
    # Send the request
    response = requests.post(api_url, files=files, data=data, auth=auth)
    
    # Close the opened file
    files['sequence-file'].close()
    
    # Handle the response
    if response.status_code == 200:
        result = response.json()
        return result['url']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    # API configuration
    
    username = 'your_username'
    password = 'your_password'
    
    # Task parameters
    sequence_file = r'/path/to/your.fasta'
    email = 'your_email'
    
    # Execute the PSSM generation task
    result_url = pssm_generation(sequence_file, email, username, password)
    
    # Output the result
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("PSSM generation failed, please check your input and error messages.")
