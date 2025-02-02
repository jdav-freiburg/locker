import json

from webdav3.client import Client
from pathlib import Path
import os
from datetime import datetime
import time
import re
from filelock import FileLock

# Configuration
nextcloud_url = "https://cloud.jdav-freiburg.de/remote.php/dav/files/depot"
api_token = "pwERt-no4Cd-gQQ3A-sQpqc-ZxHz4"
username = "depot"
local_file_paths = []
remote_file_paths = []

# WebDAV client setup
options = {
    'webdav_hostname': nextcloud_url,
    'webdav_login': username,
    'webdav_password': api_token
}

client = Client(options)

def get_sync_files_from_json():
    global local_file_paths
    global remote_file_paths
    config_path = os.getenv("config_path")
    with open(config_path) as json_file:
        conf = json.load(json_file)
    local_file_paths = conf["database"]["local_path"]
    remote_file_paths = conf["database"]["remote_path"]

# Upload a file
def upload_file(local_path, remote_path):
    try:
        if not Path(local_path).exists():
            print(f"Local file '{local_path}' does not exist.")
            return
        client.upload_sync(remote_path=remote_path, local_path=local_path)
        print(f"File '{local_path}' successfully uploaded to '{remote_path}' on Nextcloud.")
    except Exception as e:
        print(f"An error occurred: {e}")

# download_file
def download_file(remote_path, local_path):
    try:
        client.download_sync(remote_path=remote_path, local_path=local_path)
        print(f"File downloaded")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_more_recent(remote_path, local_path):
    more_recent = client.is_local_more_recent(local_path, remote_path)
    print(f"{more_recent}")


def changed_since_last_sync(local_path, remote_path, last_sync):
    last_local_change = os.path.getmtime(local_path)
    last_remot_change = client.info(remote_path)["modified"]
    last_remote_time = datetime.strptime(last_remot_change, "%a, %d %b %Y %H:%M:%S %Z").timestamp()
    print(f"{last_remote_time}")
    print(f"{last_local_change}")
    print(f"{last_sync}")
    if last_sync < last_remote_time and last_sync < last_local_change:
        return True
    else:
        return False


def sync_files(remote_path, local_path, last_sync):
    both_changed_since_last_sync = changed_since_last_sync(local_path, remote_path, last_sync)
    if both_changed_since_last_sync:
        sync_with_merge(remote_path, local_path)
    else:
        sync_without_backup(remote_path, local_path)

def sync_without_backup(remote_path, local_path):
    local_more_recent = client.is_local_more_recent(local_path, remote_path)
    if local_more_recent:
        upload_file(local_path, remote_path)
    else:
        download_file(remote_path, local_path)

def sync_with_merge(remote_path, local_path):
    remote_merge_file_path = "../../for_merge.txt"
    download_file(remote_path, remote_merge_file_path)
    merged_data = []
    pattern = r"\s+"
    with open(local_path, "r") as local_file, open(remote_merge_file_path, "r") as remote_merge_file:
        for line_local, line_remote in zip(local_file, remote_merge_file):
            if line_local == line_remote:
                merged_data.append(line_local)
            else:
                if re.match(pattern, line_local) and not re.match(pattern, line_remote):
                    merged_data.append(line_local)
                elif not re.match(pattern, line_local) and re.match(pattern, line_remote):
                    merged_data.append(line_remote)
                else:
                    merged_data.append(line_local)
                    merged_data.append(line_remote)
    with open(local_path, "w") as local_file:
        local_file.writelines(merged_data)

    upload_file(local_path, remote_path)

def poll_changes():
    last_sync = time.time()
    get_sync_files_from_json()
    old_local_changes = [os.path.getmtime(local_file) for local_file in local_file_paths]
    old_remote_changes = [
        datetime.strptime(client.info(remote_file)["modified"], "%a, %d %b %Y %H:%M:%S %Z").timestamp()
        for remote_file in remote_file_paths
    ]

    while True:
        local_changes = [os.path.getmtime(local_file) for local_file in local_file_paths]
        remote_changes = [
            datetime.strptime(client.info(remote_file)["modified"], "%a, %d %b %Y %H:%M:%S %Z").timestamp()
            for remote_file in remote_file_paths
        ]

        for i, (local_file, remote_file) in enumerate(zip(local_file_paths, remote_file_paths)):
            if old_local_changes[i] < local_changes[i] or old_remote_changes[i] < remote_changes[i]:
                lock = FileLock("lock_" + local_file)
                with lock:
                    sync_files(remote_file, local_file, last_sync)
                # Update timestamps after sync
                local_changes[i] = os.path.getmtime(local_file)
                remote_changes[i] = datetime.strptime(client.info(remote_file)["modified"],
                                                      "%a, %d %b %Y %H:%M:%S %Z").timestamp()
                old_local_changes[i] = local_changes[i]
                old_remote_changes[i] = remote_changes[i]
                last_sync = time.time()

        time.sleep(3)

# Run the upload
poll_changes()
