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
    check_file_changes(root, lambda x: x, lambda x: x)
    # dry running check_file_changes ensures we have a map
    # of how the file system looks on initiation
    # if we do not run this we will emit creation events for every file
    while True:
        check_file_changes(root, change_callback, create_callback)
        check_for_delition(delete_callback)
        time.sleep(rest)


hashes = {}
def check_for_delition(callback):
    deleted = []
    for path in hashes:
        if not os.path.exists(path):
            callback(path)
            deleted.append(path)
    for path in deleted:
        del hashes[path]

def check_file_changes(root, change_callback, create_callback):
    for node in os.listdir(root):
        path = root + "/" + node
        is_directory = os.path.isdir(path)
        if is_directory:
            hashes[path] = "0"
            check_file_changes(path, change_callback, create_callback)
            continue

        file_was_created = not hashes.get(path)
        if file_was_created:
            hashes[path] = calculate_file_hash(path)
            create_callback(path)
            continue

        file_was_changed = hashes[path] != calculate_file_hash(path)
        if file_was_changed:
            hashes[path] = calculate_file_hash(path)
            change_callback(path)


def calculate_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()
        


if __name__ == "__main__":
    main()
