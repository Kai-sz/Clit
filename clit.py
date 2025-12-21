import os
from change_detection import watch_file_changes
import subprocess

def main():
    clit_init()
    watch_file_changes(".",
        handle_update,
        handle_create,
        handle_delete
    )

def clit_init():
    if not os.path.exists(".clit"):
        os.mkdir(".clit")
    if not os.path.exists(".clit/mirror"):
        os.mkdir(".clit/mirror")


def handle_update(path):
    gen_delta(path)

def handle_create(path):
    add_to_mirror(path)

def handle_delete(path):
    print("deletou", path)

def gen_delta(path):
    mirror_path = get_mirror_path(path)
    delta = calculate_delta(path, mirror_path)
    delta_id = hash_object(delta)
    print("mudou", path)
    print(delta_id)
    return delta


def get_mirror_path(path):
    path = path[2:] if path.startswith("./") else path
    mirror_path = f".clit/mirror/{path}"
    return mirror_path


def calculate_delta(file1, file2):
    command = f"diff {file1} {file2}"
    delta = subprocess.run(
        command,
        capture_output=True,
        shell=True,
        text=True
    ).stdout
    return delta

def hash_object(content):
    command = "git hash-object -w --stdin"
    hash_id = subprocess.run(
        command,
        input=content.encode("utf-8"),
        capture_output=True,
        shell=True,
    ).stdout
    return hash_id

def add_to_mirror(path):
    mirror_path = get_mirror_path(path)
    print("creating", mirror_path)
    if os.path.isdir(path):
        os.mkdir(mirror_path)
        return
    content = b""
    with open(path, "rb") as file:
        content = file.read()
    with open(mirror_path, "wb") as file:
        file.write(content)

if __name__=="__main__":
    main()
