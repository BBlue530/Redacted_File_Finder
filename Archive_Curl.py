import subprocess
import re
from Variables import total_filtered_urls
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
    pattern = r"\.(xls|xlsx|pdf|sql|doc|docx|pptx|zip|tar|gz|tgz|bak|7z|rar|db|backup|exe|dll|bin|bat|sh|deb|rpm|iso|img|apk|msi|dmg|tmp|crt|pem|key|pub|asc|txt|csv|log|md|json|xml|jpg|bmp|tiff|avi|mov|mkv|dwg|dxf|ai|psd|sketch|html|css|js|iso|img|ova|ovf|tar.gz|tar.xz|zipx|bz2|xz|lzma|epub|mobi|azw3|obj|stl|fbx|dae|3ds|ply|ogg|flac|wav|aac|ini|conf|yml|yaml|properties|out|err)$"
    global total_filtered_urls

    with open("unfiltered_urls.txt", "r") as file:
        urls = file.readlines()

    filtered_urls = [url.strip() for url in urls if re.search(pattern, url)]

    with open("filtered_urls.txt", "w") as filtered_file:
        for url in filtered_urls:
            total_filtered_urls += 1
            filtered_file.write(url + "\n")
    return total_filtered_urls