import os
import hashlib
import time

def main():
    print("")
    # Usage
    detect_file_changes("example.txt", lambda: print("file changed"))


def detect_file_changes(file_path, callback, rest=1):
    last_hash = calculate_file_hash(file_path)
    while True:
        current_hash = calculate_file_hash(file_path)
        if current_hash != last_hash:
            callback()
            last_hash = current_hash
        time.sleep(rest)


def calculate_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()
        


if __name__ == "__main__":
    main()