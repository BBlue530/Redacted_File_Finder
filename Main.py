from File_Download import download_files
from Snapshot_Check import check_snapshots
from Archive_Curl import curl_archive, filter_urls

domain = input("Enter Website: ")
curl_archive(domain)
filtered_url = filter_urls()
successful_snapshot = check_snapshots(filtered_url)
download_files(successful_snapshot)