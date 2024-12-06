import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def enzyme_self_calc(ec_number, email, username, password,output_file_name=None):

    api_url = 'https://www.mtc-lab.cn/enzyme_register/api/enzyme_self_calc/'
    auth = HTTPBasicAuth(username, password)
    data = {
        'ec-number': ec_number,
        'email': email
    }
    
    response = requests.post(api_url, json=data, auth=auth)
    
    if response.status_code == 200:
        result = response.json()
        result_url = result['url']
        timestamp = result_url.split('/')[-1]
        web_host = "https://www.mtc-lab.cn"
        download_url = f"{web_host}/static/enzyme_database/{timestamp}.csv"
        if output_file_name is None:
            output_file_name = timestamp + ".csv"
        else:
            output_file_name = output_file_name + ".csv"
        download_file(download_url,output_file_name)    
        return download_url
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
if __name__ == "__main__":
    ec_number = "1.1.1.1"
    email = "your_email@example.com"
    username = 'your_username'
    password = 'your_password'
    output_file_name = 'your_output_file_name.csv'
    
    result = enzyme_self_calc(ec_number, email, username, password,output_file_name)
    if result:
        if result['success']:
            print(f"Calculation successful. Result URL: https://www.mtc-lab.cn/{result['url']}")
        else:
            print(f"Calculation failed. Error: {result['error']}")
    else:
        print("API request failed.")
