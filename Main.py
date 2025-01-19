from File_Download import download_files
from Snapshot_Check import check_snapshots
from Archive_Curl import curl_archive, filter_urls

domain = input("Enter Website: ")
curl_archive(domain)
filter_urls()
check_snapshots()
download_files()