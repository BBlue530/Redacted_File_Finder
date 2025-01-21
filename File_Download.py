import subprocess
import os
import time
from Variables import total_download_try, successful_download, unsuccessful_download

VALID_EXTENSIONS = [
    'xls', 'xlsx', 'pdf', 'sql', 'doc', 'docx', 'pptx', 'zip', 'tar', 'gz', 'tgz', 
    'bak', '7z', 'rar', 'db', 'backup', 'exe', 'dll', 'bin', 'bat', 'sh', 'deb', 
    'rpm', 'iso', 'img', 'apk', 'msi', 'dmg', 'tmp', 'crt', 'pem', 'key', 'pub', 
    'asc', 'txt', 'csv', 'log', 'md', 'json', 'xml', 'jpg', 'bmp', 'tiff', 
    'avi', 'mov', 'mkv', 'dwg', 'dxf', 'ai', 'psd', 'sketch', 'html', 'css', 'js', 
    'iso', 'img', 'ova', 'ovf', 'tar.gz', 'tar.xz', 'zipx', 'bz2', 'xz', 'lzma', 'epub', 
    'mobi', 'azw3', 'obj', 'stl', 'fbx', 'dae', '3ds', 'ply', 'ogg', 'flac', 'wav', 'aac', 
    'ini', 'conf', 'yml', 'yaml', 'properties', 'out', 'err',
]

def download_file(url, download_folder, retries=3, timeout=30):
    global unsuccessful_download
    global successful_download
    global total_download_try
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
            successful_download += 1
            total_download_try += 1
            print(f"Successful: {successful_download} Unsuccessful: {unsuccessful_download} Total Downloads Tried: {total_download_try} Total Downloads To Try: {total_valid_snapshots}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Attempt: {attempt + 1} Failed to download: {file_name} from: {url}. Error: {e}")
            print(f"Successful: {successful_download} Unsuccessful: {unsuccessful_download} Total Downloads Tried: {total_download_try} Total Downloads To Try: {total_valid_snapshots}")

        except Exception as e:
            print(f"Attempt: {attempt + 1} Error while downloading: {file_name} from: {url}: {e}")
            print(f"Successful: {successful_download} Unsuccessful: {unsuccessful_download} Total Downloads Tried: {total_download_try} Total Downloads To Try: {total_valid_snapshots}")

        
        attempt += 1
        time.sleep(5)

    unsuccessful_download += 1
    total_download_try += 1
    print(f"Failed to download: {file_name} after: {retries} attempts.")
    print(f"Successful: {successful_download} Unsuccessful: {unsuccessful_download} Total Downloads Tried: {total_download_try} Total Downloads To Try: {total_valid_snapshots}")
    return False

def download_files(successful_snapshot):
    global total_valid_snapshots
    total_valid_snapshots = successful_snapshot
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