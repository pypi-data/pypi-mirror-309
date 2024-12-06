import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def ddg_predict(pdb_file_path, chain, email,  username, password, outfile=None):
    """
    This function sends a POST request to the ThermoDDG API to calculate protein stability changes.
    
    Parameters:
    - pdb_file_path (str): Path to the PDB file.
    - chain (str): Chain identifier for the PDB file.
    - email (str): Email address for receiving the results.
    - username (str): Username for basic authentication.
    - password (str): Password for basic authentication.
    - outfile (str, optional): Output file name without extension. If not provided,
                             the timestamp from the API response will be used.
    
    Returns:
    - str: Download URL if successful, None otherwise.
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/km/api/thermoDDG/'
    
    with open(pdb_file_path, 'rb') as pdb_file:
        files = {'pdb_file': pdb_file}
        data = {'chain': chain, 'email': email}
        response = requests.post(api_url, files=files, data=data, auth=auth)
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            print(f"ThermoDDG calculation started. Results will be sent to {email}")
            print(f"You can check the results at: {result['url']}")
            result_url = result['url']
            timestamp = result_url.split('/')[-1]
            download_url = f"https://www.mtc-lab.cn/static/mutation/thermoDDG/{timestamp}.csv"

            if outfile:
                file_name = outfile + '.csv'
            else:
                file_name = f"{timestamp}.csv"
            download_file(download_url, file_name)
            print(f"Downloaded file saved to: {file_name}")
            return download_url
        else:
            print(f"Error: {result['error']}")
            return None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    username = 'your_username'
    password = 'your_password'
    pdb_file_path = r'/path/to/your.pdb'
    chain = 'A'
    email = 'your_email@example.com'
    outfile = "your_out_file"
    
    ddg_predict(pdb_file_path, chain, email, username, password, outfile)
