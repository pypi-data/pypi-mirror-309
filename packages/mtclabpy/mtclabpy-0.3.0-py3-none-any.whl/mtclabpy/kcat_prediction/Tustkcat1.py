import requests
import os

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"File downloaded to: {local_filename}")

def call_calculate2_api(api_url, file_path, json_path, email, username, password):
    """
    Call the calculate2 API to process the provided text and JSON files.

    This function sends a POST request to the API with the specified files and email,
    along with the user's authentication credentials. The API processes the files and
    returns a URL where the results can be viewed.

    Parameters:
    - api_url (str): The URL of the calculate2 API.
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
        result = response.json()
        return result['url']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def Tustkcat1(username, password, email, file_path, json_path,out_file=None):

    web_site = "https://www.mtc-lab.cn"
    # Construct the API endpoint URL
    api_url = web_site + "/km/api/calculate2_v2/"

    # Call the API function
    result_url = call_calculate2_api(api_url, file_path, json_path, email, username, password)

    if result_url:
        print(f"You can view the result at this URL: {web_site}{result_url}")
        file_url = web_site + r'/static/result/km2/' + result_url.split("/")[-1] + '.csv'

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
    email = "your_email@example.com"
    file_path = "/path/to/your/input.txt"
    json_path = "/path/to/your/config.json"
    out_file = "your_out_file"

    Tustkcat1(username, password, email, file_path, json_path,out_file)
