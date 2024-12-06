import requests
from requests.auth import HTTPBasicAuth
import os


def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def pssm_result_2_excel(pssm_file, username, password,outfile_name=None):
    """
    This function sends a POST request to the PSSM Result to Excel API to convert a PSSM file to Excel format.
    
    Parameters:
    - pssm_file (str): Path to the PSSM file.
    - api_url (str): URL of the PSSM Result to Excel API.
    - username (str): Username for basic authentication.
    - password (str): Password for basic authentication.
    
    Returns:
    - str: URL to the converted Excel file if the request is successful, otherwise None.
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/mutation/api/pssm_result_2_excel/'
    
    # Prepare the file to upload
    files = {'pssm_file': open(pssm_file, 'rb')}
    
    # Send the request
    response = requests.post(api_url, files=files, auth=auth)
    
    # Close the opened file
    files['pssm_file'].close()
    
    # Handle the response
    if response.status_code == 200:
        result = response.json()
        result_url = result['url']
        web_host = "https://www.mtc-lab.cn"
        download_url = f"{web_host}{result_url}"
        if not outfile_name:
            outfile_name = result_url.split('/')[-1]
        else:
            outfile_name = outfile_name+'.xlsx'
        download_file(download_url, outfile_name)
        return download_url
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    
    username = 'your_username'
    password = 'your_password'
    pssm_file = r'/path/to/your.pssm'
    outfile_name = 'your_output_file_name'
    
    result_url = pssm_result_2_excel(pssm_file, username, password,outfile_name=outfile_name)
    if result_url:
        print(f"You can download the Excel file at this URL: {result_url}")
    else:
        print("Conversion failed, please check your input and error messages.")
