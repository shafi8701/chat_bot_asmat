import shutil

def move_file(src, dest):
    shutil.move(str(src), str(dest))