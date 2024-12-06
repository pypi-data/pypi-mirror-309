import requests
from requests.auth import HTTPBasicAuth
import os

def ctr_project(pssm_file, seq_file, positions_file, email, username, password):
    """
    This function sends a POST request to the Calculate1 API to perform calculations based on PSSM, sequence, and positions files.
    
    Parameters:
    - pssm_file (str): Path to the PSSM file.
    - seq_file (str): Path to the sequence file.
    - positions_file (str): Path to the positions file.
    - email (str): Email address for the API request.
    - username (str): Username for basic authentication.
    - password (str): Password for basic authentication.
    
    Returns:
    - str: URL to the result if the request is successful, otherwise None.
    """
    auth = HTTPBasicAuth(username, password)
    api_url = 'https://www.mtc-lab.cn/mutation/api/calculate1/'
    
    files = {
        'pssm': open(pssm_file, 'rb'),
        'seq': open(seq_file, 'rb'),
        'positions': open(positions_file, 'rb')
    }
    
    data = {
        'email': email,
    }
    
    response = requests.post(api_url, files=files, data=data, auth=auth)
    
    for file in files.values():
        file.close()
    
    if response.status_code == 200:
        result = response.json()
        return result['url']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Usage example
# 测试代码示例
if __name__ == "__main__":
    
    username = 'your_username'
    password = 'your_password'

    # 确保三个文件的基本名称相同，例如：
    pssm_file = '/path/to/your.pssm'
    seq_file = '/path/to/your_sequence'
    positions_file = '/path/to/your_positions.txt'
    email = 'your_email@example.com'
    
    result_url = ctr_project(pssm_file, seq_file, positions_file, email, username, password)
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")
