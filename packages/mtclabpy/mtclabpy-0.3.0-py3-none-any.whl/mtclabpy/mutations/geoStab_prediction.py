import requests
from requests.auth import HTTPBasicAuth



def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def geoStab_prediction(pdb_file_path, chain_id, mut_pos, mut_res,  username, password, email,outfile_name=None):
    """
    Predict protein stability changes using GeoStab.
    
    Args:
        pdb_file_path (str): Path to PDB structure file
        chain_id (str): Chain identifier in the PDB file
        mut_pos (str): Position of the mutation
        mut_res (str): Target residue for mutation
        api_url (str): API endpoint URL
        username (str): Your API username
        password (str): Your API password
        email (str): Email address to receive results
        
    Returns:
        str: URL to access the results
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
                        outfile_name = file_name
                    else:
                        outfile_name = outfile_name+'_'+file_name
                    download_file(download_url, outfile_name)
                    print(f"Downloaded {file_name} successfully")
                except Exception as e:
                    print(f"Error downloading {file_name}: {str(e)}")
            return result['url']
        else:
            print(f"Error: {response.status_code}")
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
    
    result_url = geoStab_prediction(
        pdb_file,
        chain_id,
        mut_pos,
        mut_res,
        username,
        password,
        email
    )
    
    if result_url:
        print(f"Results will be available at: {result_url}")
