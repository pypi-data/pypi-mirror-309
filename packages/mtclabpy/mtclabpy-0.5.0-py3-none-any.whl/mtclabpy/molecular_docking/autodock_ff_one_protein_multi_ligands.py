import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def autodock_ff_one_protein_multi_ligands(protein_file, ligand_files, p1, p2, email, username, password, output_file_name=None):
    """
    This function sends a POST request to the AutoDock FF API to perform docking calculations for one protein and multiple ligands.

    Parameters:
    - protein_file (str): Path to the protein file (PDB format).
    - ligand_files (list): List of paths to the ligand files (SDF format).
    - p1 (str): Parameter 1 for the docking calculation (e.g., grid dimensions).
    - p2 (str): Parameter 2 for the docking calculation (e.g., grid center coordinates).
    - email (str): Email address for receiving the results.
    - username (str): Username for basic authentication.
    - password (str): Password for basic authentication.
    - output_file_name (str, optional): Custom name for the output file. If not provided, the timestamp from the response will be used.

    Returns:
    - str: URL to the downloaded result file if the request is successful, otherwise None.
    """
    api_url = 'https://www.mtc-lab.cn/km/api/autodock_ff_one_protein_multi_ligands/'
    auth = HTTPBasicAuth(username, password)

    # Prepare files to upload
    files = {
        'protein_file': open(protein_file, 'rb'),
    }
    
    # 修改这里：使用相同的键名'ligand_file'上传多个文件
    for ligand_file in ligand_files:
        # 注意：这里不再使用索引，而是使用相同的键名'ligand_file'
        files['ligand_file'] = open(ligand_file, 'rb')

    # Prepare request data
    data = {
        'email': email,
        'p1': p1,
        'p2': p2,
    }

    try:
        # Send the request
        response = requests.post(api_url, files=files, data=data, auth=auth)

        # Handle the response
        if response.status_code == 200:
            result = response.json()
            result_url = result['url']
            timestamp = result_url.split('/')[-1]
            web_host = "https://www.mtc-lab.cn"
            download_url = web_host + f"/static/docking_md/autodock_ff_one_protein_multi_ligands/{timestamp}/{timestamp}.zip"

            if output_file_name is None:
                output_file_name = timestamp + ".zip"
            else:
                output_file_name = output_file_name + ".zip"

            download_file(download_url, output_file_name)
            print(f"Results downloaded to: {output_file_name}")

            return download_url
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
            
    finally:
        # Close all opened files
        for file in files.values():
            file.close()

if __name__ == "__main__":
    # API配置
    
    username = 'your_username'
    password = 'your_password'
    
    # 任务参数
    protein_file = '/path/to/your/protein.pdb'
    ligand_files = [
        '/path/to/your/ligand1.sdf',
        '/path/to/your/ligand2.sdf'
    ]
    p1 = '80,64,64'
    p2 = '-15,15,129'
    email = 'your_email@example.com'
    output_file_name = None
    
    # 执行对接任务
    result_url = autodock_ff_one_protein_multi_ligands(
        protein_file, 
        ligand_files, 
        p1, 
        p2, 
        email, 
        username, 
        password,
        output_file_name
    )
    
    # 输出结果
    if result_url:
        print(f"You can view the result at this URL: {result_url}")
    else:
        print("Calculation failed, please check your input and error messages.")