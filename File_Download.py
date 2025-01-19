import subprocess
import os
import time

VALID_EXTENSIONS = [
    'xls', 'xlsx', 'pdf', 'sql', 'doc', 'docx', 'pptx', 'zip', 'tar', 'gz', 'tgz',
    'bak', '7z', 'rar', 'db', 'backup', 'exe', 'dll', 'bin', 'bat', 'sh', 'deb', 'rpm',
    'iso', 'img', 'apk', 'msi', 'dmg', 'tmp', 'crt', 'pem', 'key', 'pub', 'asc'
]

def download_file(url, download_folder, retries=3, timeout=30):
    file_name = url.split("/")[-1]
    file_extension = file_name.split('.')[-1] if '.' in file_name else None

    if not file_extension or file_extension not in VALID_EXTENSIONS:
        file_name = f"{file_name}.zip"
    
    file_path = os.path.join(download_folder, file_name)

    os.makedirs(download_folder, exist_ok=True)

    curl_command = [
        "curl", "-L", "-o", file_path, url, "--max-time", str(timeout)
    ]
    
    attempt = 0
    while attempt < retries:
        try:
            subprocess.run(curl_command, check=True)
            print(f"Downloaded: {file_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Attempt: {attempt + 1} Failed to download: {file_name} from: {url}. Error: {e}")
        except Exception as e:
            print(f"Attempt: {attempt + 1} Error while downloading: {file_name} from: {url}: {e}")
        
        attempt += 1
        time.sleep(5)

    print(f"Failed to download: {file_name} after: {retries} attempts.")
    return False

def download_files():
    with open("valid_urls.txt", "r") as valid_file:
        valid_urls = [url.strip() for url in valid_file.readlines()]

    download_folder = "downloaded_files"
    os.makedirs(download_folder, exist_ok=True)

    successful_downloads = 0
    failed_downloads = 0

    for url in valid_urls:
        success = download_file(url, download_folder)
        if success:
            successful_downloads += 1
        else:
            failed_downloads += 1

    print(f"Finished downloading files. {successful_downloads} files downloaded.")
    print(f"{failed_downloads} downloads failed.")