import requests
from requests.auth import HTTPBasicAuth
import os

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def pssm_organize(pssm_file, username, password, outfile_name=None):
    """
    Convert a PSSM file to Excel format for better organization and analysis.
    
    Parameters:
    - pssm_file (str): Path to the PSSM file.
    - username (str): Username for basic authentication.
    - password (str): Password for basic authentication.
    - outfile_name (str, optional): Name for the output Excel file (without extension).
                                  If not provided, will use the original filename.
    
    Returns:
    - str: URL to the converted Excel file if the request is successful, otherwise None.
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/mutation/api/pssm_result_2_excel/'
    
    # Prepare the file to upload
    with open(pssm_file, 'rb') as f:
        files = {'pssm_file': f}
        
        # Send the request
        response = requests.post(api_url, files=files, auth=auth)
    
    # Handle the response
    if response.status_code == 200:
        result = response.json()
        if not result.get('success', True):  # Check for API-level errors
            print(f"API Error: {result.get('error', 'Unknown error')}")
            return None
            
        result_url = result['url']
        web_host = "https://www.mtc-lab.cn"
        download_url = f"{web_host}{result_url}"
        
        # Determine output filename
        if not outfile_name:
            outfile_name = os.path.splitext(os.path.basename(pssm_file))[0]
        save_name = f"{outfile_name}.xlsx"
        
        try:
            download_file(download_url, save_name)
            print(f"Downloaded Excel file to: {save_name}")
            return download_url
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    username = 'your_username'
    password = 'your_password'
    pssm_file = r'/path/to/your.pssm'
    outfile_name = 'my_pssm_analysis'
    
    result_url = pssm_organize(pssm_file, username, password, outfile_name)
    if result_url:
        print(f"You can download the Excel file at: {result_url}")
    else:
        print("Conversion failed, please check the error messages above.")
