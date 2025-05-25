import os
import shutil

from textnode import *

def prepare_directory(source, destination):
    if not os.path.exists(source) or os.listdir(source) == []:
        print(f"Source '{source}' directory either does not exist or is empty. Aborting as there's nothing to populate with.")
        return
    
    if os.path.exists(destination):
        print(f"Destination '{destination}' exists, but isn't empty. Recreating it.")
        shutil.rmtree(destination)
        os.mkdir(destination)
    else:
        print(f"Destination '{destination}' doesn't exist. Creating it.")
        os.mkdir(destination)

    source_contents = os.listdir(source)
    if source_contents != []:
        for obj in source_contents:
            obj_path = os.path.join(source, obj)
            dest_path = os.path.join(destination, obj)
            if os.path.isfile(obj_path):
                print(f"Copying {obj_path} to {destination}.")
                shutil.copy(obj_path, dest_path)
            else:
                print(f"Processing {obj_path}.")
                prepare_directory(obj_path, dest_path)

def main():
    prepare_directory("static", "public")

main()