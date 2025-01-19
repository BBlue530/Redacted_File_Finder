import subprocess
import re

def curl_archive(domain):
    curl_command = [
        "curl", "-G", "https://web.archive.org/cdx/search/cdx",
        "--data-urlencode", f"url=*.{domain}/*",
        "--data-urlencode", "collapse=urlkey",
        "--data-urlencode", "output=text",
        "--data-urlencode", "fl=original"
    ]

    with open("unfiltered_urls.txt", "w") as out_file:
        subprocess.run(curl_command, stdout=out_file)

def filter_urls():
    pattern = r"\.(xls|xlsx|pdf|sql|doc|docx|pptx|zip|tar|gz|tgz|bak|7z|rar|db|backup|exe|dll|bin|bat|sh|deb|rpm|iso|img|apk|msi|dmg|tmp|crt|pem|key|pub|asc)$"

    with open("unfiltered_urls.txt", "r") as file:
        urls = file.readlines()

    filtered_urls = [url.strip() for url in urls if re.search(pattern, url)]

    with open("filtered_urls.txt", "w") as filtered_file:
        for url in filtered_urls:
            filtered_file.write(url + "\n")