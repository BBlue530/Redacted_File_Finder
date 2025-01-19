import requests
import concurrent.futures

def check_snapshot(url):
    snapshot_api = f"https://archive.org/wayback/available?url={url}"
    timeout_duration = 10
    try:
        response = requests.get(snapshot_api, timeout=timeout_duration)
        print(f"GET request to {snapshot_api}")

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} Url: {url}")
            return (url, None, False)

        try:
            data = response.json()
        except ValueError:
            print(f"Error: Invalid JSON response: {url}")
            return (url, None, False)

        if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
            snapshot = data["archived_snapshots"]["closest"]
            status = snapshot.get("status")
            timestamp = snapshot.get("timestamp")

            if status == "200":
                archived_url = f"http://web.archive.org/web/{timestamp}/{url}"
                print(f"Snapshot found for: {url}")
                return (url, archived_url, True)
            else:
                print(f"Snapshot for: {url} not available Status: {status}")
                return (url, None, False)
        else:
            print(f"No snapshot for: {url}")
            return (url, None, False)

    except requests.exceptions.Timeout:
        print(f"Request to: {url} timed out after {timeout_duration} seconds.")
        return (url, None, False)
    except Exception as e:
        print(f"Error: {url}: {e}")
        return (url, None, False)

def check_snapshots():
    with open("filtered_urls.txt", "r") as file:
        filtered_urls = file.readlines()

    valid_urls = []
    invalid_urls = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(check_snapshot, url.strip()): url.strip() for url in filtered_urls}

        for future in concurrent.futures.as_completed(futures):
            url, archived_url, is_valid = future.result()
            if is_valid:
                valid_urls.append(archived_url)
            else:
                invalid_urls.append(url)

    with open("valid_urls.txt", "w") as valid_file:
        for archived_url in valid_urls:
            valid_file.write(archived_url + "\n")

    with open("invalid_urls.txt", "w") as invalid_file:
        for invalid_url in invalid_urls:
            invalid_file.write(invalid_url + "\n")

    print(f"Finished checking valid URL.")