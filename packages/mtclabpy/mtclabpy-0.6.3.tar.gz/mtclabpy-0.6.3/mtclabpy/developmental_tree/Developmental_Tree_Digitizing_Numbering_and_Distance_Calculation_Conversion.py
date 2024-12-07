import requests
from requests.auth import HTTPBasicAuth
import os

def tree_file_conversion(tree_file, email, username, password, out_dir, tree_build_file, tree_build_matrix_file):
    """
    Convert a phylogenetic tree file to CSV format and download the results.
    
    This function uploads a tree file to the API for conversion and downloads 
    the resulting CSV files to a specified directory.
    
    Args:
        tree_file (str): Path to the input tree file
        email (str): Email address for receiving results
        username (str): API authentication username
        password (str): API authentication password
        out_dir (str): Output directory for saving results
        tree_build_file (str): Name for the tree build output file
        tree_build_matrix_file (str): Name for the matrix output file
    
    Returns:
        str: URL to access the results, or None if conversion fails
        
    Notes:
        - Ensure the input tree file is in a valid format
        - The output directory must have write permissions
        - Valid API credentials are required for authentication
    """
    # API base configuration
    web_site = 'https://www.mtc-lab.cn/'
    api_url = web_site + '/USalign/api/tree_file_conversion/'
    auth = HTTPBasicAuth(username, password)
    
    # Prepare upload files and data
    files = {'tree_file': open(tree_file, 'rb')}
    data = {
        'email': email,
    }
    
    # Send API request
    response = requests.post(api_url, files=files, data=data, auth=auth)
    files['tree_file'].close()
    
    if response.status_code == 200:
        # Process successful response
        result = response.json()
        result_url = result['url']
        timestamp = result_url.split('/')[-1]
        
        # Construct download URLs
        tree_build_file = f"https://www.mtc-lab.cn/static/Tree_build/{timestamp}/tree_build.csv"
        tree_build_matrix_file = f"https://www.mtc-lab.cn/static/Tree_build/{timestamp}/tree_build_matrix.csv"
        
        # Download tree build file
        tree_build_response = requests.get(tree_build_file)
        if tree_build_response.status_code == 200:
            tree_build_path = os.path.join(out_dir, f"{tree_build_file}.csv")
            with open(tree_build_path, "wb") as f:
                f.write(tree_build_response.content)
        
        # Download matrix file
        matrix_response = requests.get(tree_build_matrix_file)
        if matrix_response.status_code == 200:
            matrix_path = os.path.join(out_dir, f"{tree_build_matrix_file}.csv") 
            with open(matrix_path, "wb") as f:
                f.write(matrix_response.content)
        
        return result_url
    else:
        # Handle error response
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example usage
if __name__ == "__main__":
    # API authentication configuration
    username = '****'  # Replace with your username
    password = '****'  # Replace with your password
    email = '****@**.**'  # Replace with your email
    
    # File path configuration
    tree_file = "path/to/your/tree/file"  # Replace with your tree file path
    out_path = "path/to/output/directory"  # Replace with your output directory
    tree_build_file = "your_tree_build.csv"  # Tree build file name
    tree_build_matrix_file = "your_tree_build_matrix.csv"  # Matrix file name

    # Execute conversion
    result_url = tree_file_conversion(
        tree_file, email, username, password, 
        out_path, tree_build_file, tree_build_matrix_file
    )    
    
    # Output results
    if result_url:
        print(f"Success! View results at: {result_url}")
    else:
        print("Conversion failed. Please check your inputs and error messages.")
