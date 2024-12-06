import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def nessolp(fasta_file_path, email, username, password,output_file_name=None):
    
    api_url = 'https://www.mtc-lab.cn/SolP/api/create_chemical_compound_2/'
    auth = HTTPBasicAuth(username, password)
    with open(fasta_file_path, 'rb') as fasta_file:
        files = {'fasta': fasta_file}
        data = {'email': email}
        try:
            print(f"Sending request to: {api_url}")
            response = requests.post(api_url, files=files, data=data, auth=auth)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            return None
    
    if response.status_code == 200:
        result = response.json()
        result_url = result.get('url')
        timestamp = result_url.split('/')[-1]
        web_host = "https://www.mtc-lab.cn"
        download_url = f"{web_host}/static/result/SolP/Calculation1/{timestamp}.csv"
        if output_file_name is None:
            output_file_name = timestamp + ".csv"
        else:
            output_file_name = output_file_name + ".csv"
        download_file(download_url,output_file_name)
        return download_url
    else:
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

# Usage example
if __name__ == "__main__":
    fasta_file_path = "/path/to/your/sequence.fasta"
    email = "your_email@example.com"

    username = 'your_username'
    password = 'your_password'
    output_file_name = 'your_output_file_name.csv'

    result_url = nessolp(fasta_file_path, email, username, password,output_file_name)
    if result_url:
        print(f"Calculation successful. Result URL: {result_url}")
    else:
        print("Calculation failed.")
