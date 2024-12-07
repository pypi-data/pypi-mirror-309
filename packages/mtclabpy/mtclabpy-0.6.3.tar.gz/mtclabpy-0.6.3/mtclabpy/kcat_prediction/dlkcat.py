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

def call_calculate1_api(api_url, file_path, json_path, email, username, password):
    """
    Call the calculate1 API to process the provided text and JSON files.

    This function sends a POST request to the API with the specified files and email,
    along with the user's authentication credentials. The API processes the files and
    returns a URL where the results can be viewed.

    Parameters:
    - api_url (str): The URL of the calculate1 API.
    - file_path (str): The path to the text file to be processed.
    - json_path (str): The path to the JSON configuration file.
    - email (str): Email address for receiving the results.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.

    Returns:
    - str: The URL where the results can be viewed if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    with open(file_path, 'rb') as file, open(json_path, 'rb') as json_file:
        files = {
            'txt_file': file,
            'json_file': json_file
        }
        data = {
            'email': email
        }

        response = requests.post(
            api_url,
            files=files,
            data=data,
            auth=(username, password)
        )

        if response.status_code == 200:
            result_url = response.json().get('result_url')
            print(f"API request successful. Results available at: {result_url}")
            return result_url
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return None

def dlkcat(username, password, email, file_path, json_path, out_file):
    """
    Download and process kcat data from the BRENDA database
    
    Parameters:
        username (str): BRENDA database username
        password (str): BRENDA database password
        email (str): User's email address
        file_path (str): Input file path containing EC numbers to query
        json_path (str): Path to store the raw JSON data downloaded from BRENDA
        out_file (str): Output file path for processed kcat data
        
    Functions:
        1. Connect to BRENDA database using provided credentials
        2. Read EC numbers list from input file
        3. Retrieve kcat data for each EC number from BRENDA
        4. Save raw data in JSON format
        5. Process data and write results to output file
        
    Returns:
        None
        
    Notes:
        - Requires valid BRENDA database account
        - Ensure input file contains correctly formatted EC numbers
        - JSON file will store all raw data for subsequent analysis
    """
    # API endpoint URLs
    api_url = "https://www.brenda-enzymes.org/rest/v2/calculate1"
    result_url = call_calculate1_api(api_url, file_path, json_path, email, username, password)
    
    if result_url:
        # Download the results
        download_file(result_url, out_file)
    else:
        print("Failed to process kcat data")

# Example usage
if __name__ == "__main__":
    username = "your_username"
    password = "your_password"
    email = "your_email@example.com"
    file_path = "input.txt"
    json_path = "data.json"
    out_file = "results.txt"
    
    dlkcat(username, password, email, file_path, json_path, out_file)
