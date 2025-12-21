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

def handle_update(path):
    gen_delta(path)

def handle_create(path):
    add_to_mirror(path)

def handle_delete(path):
    print("deletou", path)

def gen_delta(path):
    mirror_path = get_mirror_path(path)
    delta = calculate_delta(path, mirror_path)
    print(delta)
    return delta


def get_mirror_path(path):
    path = path[2:] if path.startswith("./") else path
    mirror_path = f".clit/mirror/{path}"
    return mirror_path


def clit_init():
    if not os.path.exists(".clit"):
        os.mkdir(".clit")
    if not os.path.exists(".clit/mirror"):
        os.mkdir(".clit/mirror")

def calculate_delta(file1, file2):
    command = f"diff {file1} {file2}"
    delta = subprocess.run(
        command,
        capture_output=True,
        shell=True,
        text=True
    ).stdout
    return delta

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
