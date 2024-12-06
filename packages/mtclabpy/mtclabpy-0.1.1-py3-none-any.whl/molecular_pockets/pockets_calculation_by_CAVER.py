import requests
from requests.auth import HTTPBasicAuth
import os


def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    

def tunel_calculation(pdb_files, config_file, email, api_url, username, password,output_file_name=None):
    """
    Call the CAVER API to calculate protein tunnels.

    This function submits multiple protein structure files and a configuration file to calculate
    potential tunnels using CAVER. It handles the API request, authentication, and downloading
    of results.

    Parameters:
    -----------
    pdb_files : list
        List of paths to PDB files containing protein structures
    config_file : str
        Path to the configuration file for CAVER parameters
    email : str
        Email address for receiving results
    api_url : str
        URL of the API endpoint
    username : str
        Username for API authentication
    password : str
        Password for API authentication
    output_file_name : str, optional
        Custom output filename for results zip file. If not provided,
        defaults to timestamp-based name

    Returns:
    --------
    str or None
        URL where tunnel calculation results can be downloaded if successful, None if request fails

    Notes:
    ------
    - Requires valid API authentication credentials
    - Input PDB files must exist and be properly formatted
    - Results are downloaded as a zip file containing CAVER outputs
    """
    
    api_url = 'https://www.mtc-lab.cn/docking_md/api/tunel_calculation/'
    auth = HTTPBasicAuth(username, password)
    
    # 准备上传文件
    files = {
        'config_file': open(config_file, 'rb'),
    }
    for i, pdb_file in enumerate(pdb_files):
        files[f'pdb_file_{i}'] = open(pdb_file, 'rb')
    
    # 准备请求数据
    data = {
        'email': email,
    }
    
    # 发送POST请求
    response = requests.post(api_url, files=files, data=data, auth=auth)
    
    # 关闭所有打开的文件
    for file in files.values():
        file.close()
    
    # 处理响应
    if response.status_code == 200:
        result = response.json()
        timestamp = result_url.split('/')[-1]
        web_host = "https://www.mtc-lab.cn"
        download_url = f"{web_host}/static/docking_md/tunel/{timestamp}/{timestamp}.zip"
        if output_file_name is None:
            output_file_name = timestamp + ".zip"
        else:
            output_file_name = output_file_name + ".zip"
        download_file(download_url, output_file_name)
        return download_url
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# 使用示例
if __name__ == "__main__":
    
    username = 'your_username'
    password = 'your_password'
    pdb_files = ['/path/to/your/protein1.pdb', '/path/to/your/protein2.pdb']
    config_file = '/path/to/your/config.txt'
    email = 'your_email@example.com'
    output_file_name = 'your_output_file_name.zip'

    result_url = tunel_calculation(pdb_files, config_file, email,  username, password,output_file_name)
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")