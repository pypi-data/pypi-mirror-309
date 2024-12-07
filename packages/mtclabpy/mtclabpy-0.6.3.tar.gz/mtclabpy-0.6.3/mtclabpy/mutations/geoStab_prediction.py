import requests
from requests.auth import HTTPBasicAuth

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def geostab_predict(pdb_file_path, chain_id, mut_pos, mut_res, username, password, email, outfile_name=None):
    """
    Predict protein stability changes using GeoStab.
    
    Args:
        pdb_file_path (str): Path to PDB structure file
        chain_id (str): Chain identifier in the PDB file
        mut_pos (str): Position of the mutation
        mut_res (str): Target residue for mutation
        username (str): Your API username
        password (str): Your API password
        email (str): Email address to receive results
        outfile_name (str, optional): Base name for output files. If not provided,
                                    original filenames will be used.
        
    Returns:
        str: URL to access the results, or None if the request fails
    """
    # Prepare the files and data for upload
    with open(pdb_file_path, 'rb') as f:
        files = {
            'pdb_file': f
        }
        
        data = {
            'chain': chain_id,
            'mut_pos': mut_pos,
            'mut_res': mut_res,
            'email': email
        }
        api_url = 'https://www.mtc-lab.cn/km/api/Geosta/'
        
        # Make the API request
        response = requests.post(
            api_url,
            files=files,
            data=data,
            auth=HTTPBasicAuth(username, password)
        )
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            if not result.get('success', True):  # Check for API-level errors
                print(f"API Error: {result.get('error', 'Unknown error')}")
                return None
                
            result_url = result['url']
            timestamp = result_url.split('/')[-1]
            
            # Download the result files
            base_url = "https://www.mtc-lab.cn/static/mutation/Geosta/"
            files_to_download = [
                "result_dTm.txt",
                "result_ddG.txt", 
                "mut_info.csv",
                "result_fitness.csv"
            ]
            
            for file_name in files_to_download:
                download_url = f"{base_url}{timestamp}/{file_name}"
                try:
                    if not outfile_name:
                        save_name = file_name
                    else:
                        save_name = f"{outfile_name}_{file_name}"
                    download_file(download_url, save_name)
                    print(f"Downloaded {file_name} to {save_name}")
                except Exception as e:
                    print(f"Error downloading {file_name}: {str(e)}")
            return result_url
        else:
            print(f"HTTP Error: {response.status_code}")
            print(response.text)
            return None

# Usage example
if __name__ == "__main__":
    username = 'your_username'
    password = 'your_password'
    pdb_file = r'path_to_your_pdb_file'
    chain_id = 'A'
    mut_pos = '100'
    mut_res = 'A'
    email = 'your_email'
    outfile_name = 'my_prediction'
    
    result_url = geostab_predict(
        pdb_file,
        chain_id,
        mut_pos,
        mut_res,
        username,
        password,
        email,
        outfile_name
    )
    
    if result_url:
        print(f"Results will be available at: {result_url}")
