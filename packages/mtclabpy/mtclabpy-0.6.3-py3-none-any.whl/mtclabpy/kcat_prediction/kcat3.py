import requests
import os

def download_file(url, local_filename):
    """
    Download a file from a given URL and save it to the specified local filename.

    Parameters:
    - url (str): The URL of the file to download.
    - local_filename (str): The local filename to save the downloaded file.

    Returns:
    - None
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"File downloaded to: {local_filename}")

def call_calculate3_api(api_url, file_path, smiles, email, username, password):
    """
    Call the calculate3 API to process the provided file and SMILES string.

    This function sends a POST request to the API with the specified file, SMILES string, and email,
    along with the user's authentication credentials. The API processes the file and returns a URL
    where the results can be viewed.

    Parameters:
    - api_url (str): The URL of the calculate3 API.
    - file_path (str): The path to the file to be processed.
    - smiles (str): The SMILES string representing the chemical structure.
    - email (str): Email address for receiving the results.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.

    Returns:
    - str: The URL where the results can be viewed if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    with open(file_path, 'rb') as file:
        files = {'file': file}
        data = {
            'smiles': smiles,
            'email': email
        }

        response = requests.post(
            api_url,
            files=files,
            data=data,
            auth=(username, password)
        )

    if response.status_code == 200:
        result = response.json()
        return result['url']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def kcat3(username, password, smiles, email, file_path,out_file=None):
    """
    Calculate kcat values using the kcat3 API with SMILES string input
    
    Parameters:
        username (str): API authentication username
        password (str): API authentication password 
        smiles (str): SMILES string representing chemical structure
        email (str): User's email address
        file_path (str): Input file path containing enzyme data
        out_file (str, optional): Output file path for results. If not provided,
                                 will use input filename with .csv extension
        
    Functions:
        1. Authenticates with API using provided credentials
        2. Submits enzyme data file and SMILES string to API
        3. Retrieves results URL and downloads CSV results file
        4. Saves processed data to specified output file
        
    Returns:
        None
        
    Notes:
        - Requires valid API authentication credentials
        - Input file should contain properly formatted enzyme data
        - SMILES string must represent valid chemical structure
        - Results are downloaded as CSV file
    """

    web_site = "https://www.mtc-lab.cn"
    # Construct the API endpoint URL
    api_url = web_site + "/km/api/calculate3/"

    # Call the API function
    result_url = call_calculate3_api(api_url, file_path, smiles, email, username, password)

    if result_url:
        print(f"You can view the result at this URL: {web_site}/{result_url}")
        file_url = web_site + r'/static/result/km3/' + result_url.split("/")[-1] + '.csv'

        # Get the original filename
        original_filename = os.path.basename(file_path)
        # Construct new filename (keep original name but change extension to .csv)
        if not out_file:
            new_filename = os.path.splitext(original_filename)[0] + '.csv'
        else:
            new_filename = out_file+'.csv'
        # Download the file
        download_file(file_url, new_filename)
        print('Download complete!')
    else:
        print("Calculation failed, please check your input and error messages.")

# Example usage
if __name__ == "__main__":
    
    username = "your_username"
    password = "your_password"
    smiles = "your_smiles"  # Example SMILES string for acetic acid
    email = "your_email@example.com"
    file_path = "/path/to/your/input.txt"
    out_file = "your_out_file"

    kcat3(username, password, smiles, email, file_path,out_file)
