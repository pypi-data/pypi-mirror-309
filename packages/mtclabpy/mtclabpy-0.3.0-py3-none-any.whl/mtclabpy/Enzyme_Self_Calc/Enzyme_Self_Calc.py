import os
import requests
from requests.auth import HTTPBasicAuth

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

def enzyme_self_calc(ec_number, email, username, password, out_file):
    """
    Perform self-calculation for an enzyme using the Enzyme Self-Calc API.

    This function sends a POST request to the API with the provided EC number and email,
    along with the user's authentication credentials. The API processes the enzyme data and
    returns a result that includes a URL where the detailed results can be viewed.

    Parameters:
    - ec_number (str): The EC number of the enzyme to be calculated.
    - email (str): Email address for receiving the results.
    - api_url (str): URL of the Enzyme Self-Calc API.
    - username (str): Username for API authentication.
    - password (str): Password for API authentication.

    Returns:
    - dict: A dictionary containing the result of the calculation if the request is successful.
    - None: If the request fails, prints an error message and returns None.
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/enzyme_register/api/enzyme_self_calc/'

    data = {
        'ec-number': ec_number,
        'email': email
    }

    response = requests.post(api_url, json=data, auth=auth)

    if response.status_code == 200:
        result = response.json()
        ec_number = result['url'].split('-')[-1]
        out_file = f"{out_file}.csv"
        download_url = f'https://www.mtc-lab.cn/static/enzyme_database/{ec_number}.csv'
        download_file(download_url, out_file)
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    # Define the EC number, email, API URL, and authentication credentials
    ec_number = "*.*.*.*"
    email = "your_email@example.com"
    
    username = 'your_username'
    password = 'your_password'
    out_file = 'your_out_file'
    # Call the enzyme_self_calc function and store the result
    result = enzyme_self_calc(ec_number, email, username, password, out_file)

    # Check if the calculation was successful and print the result URL or an error message
    if result:
        if result['success']:
            print(f"Calculation successful. Result URL: https://www.mtc-lab.cn/{result['url']}")
        else:
            print(f"Calculation failed. Error: {result['error']}")
    else:
        print("API request failed.")
