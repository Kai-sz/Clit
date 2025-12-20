import os
from change_detection import watch_file_changes

def main():
    clit_init()

def clit_init():
    if not os.path.exists(".clit"):
        os.mkdirs(".clit")
