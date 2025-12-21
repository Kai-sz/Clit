import os
import hashlib
import time

def main():
    # Usage
    watch_file_changes(".",
        lambda path: print("mudou",path),
        lambda path: print("criou",path),
        lambda path: print("deletou",path)
    )

def watch_file_changes(root, change_callback, create_callback, delete_callback, rest = 1):
    dry_run()
    # dry running check_file_changes ensures we have a map
    # of how the file system looks on initiation
    # if we do not run this we will emit creation events for every file
    while True:
        check_file_changes(root, change_callback, create_callback)
        check_for_delition(delete_callback)
        time.sleep(rest)

def dry_run(root=".clit/mirror"):
    for node in os.listdir(root):
        path = root + "/" + node
        write_point = path.replace(".clit/mirror", ".")
        hashes[path] = calculate_file_hash(path)
        is_directory = os.path.isdir(path)
        if is_directory:
            dry_run(path)

hashes = {}
def check_for_delition(callback):
    for path in hashes.copy():
        if not os.path.exists(path):
            callback(path)
            del hashes[path]

def check_file_changes(root, change_callback, create_callback):
    if root == "./.git" or root == "./.clit":
        return
    for node in os.listdir(root):
        path = root + "/" + node
        is_directory = os.path.isdir(path)
        was_created = not hashes.get(path)

        if was_created:
            print(path)
            print(hashes)
            hashes[path] = calculate_file_hash(path)
            create_callback(path)

        if is_directory:
            check_file_changes(path, change_callback, create_callback)
            continue

        file_was_changed = hashes[path] != calculate_file_hash(path)
        if file_was_changed:
            hashes[path] = calculate_file_hash(path)
            change_callback(path)


def calculate_file_hash(file_path):
    if os.path.isdir(file_path):
        return "0"
    with open(file_path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()
        


if __name__ == "__main__":
    main()
