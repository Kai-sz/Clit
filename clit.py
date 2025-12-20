import os
from change_detection import watch_file_changes
import subprocess

def main():
    clit_init()
    print(gen_delta("test_dir/a", "test_dir/b"))

def clit_init():
    if not os.path.exists(".clit"):
        os.mkdirs(".clit")

def gen_delta(file1, file2):
    command = f"diff {file1} {file2}"
    delta = subprocess.run(
        command,
        capture_output=True,
        shell=True,
        text=True
    ).stdout
    return delta

if __name__=="__main__":
    main()
