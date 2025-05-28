import os
import shutil

from block_markdown import extract_title, markdown_to_html_node
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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown_file = file.read()

    markdown_html = markdown_to_html_node(markdown_file).to_html()
    page_title = extract_title(markdown_file)

    with open(template_path, 'r') as file:
        template_file = file.read()
    new_page = template_file.replace("{{ Title }}", page_title)
    new_page = new_page.replace("{{ Content }}", markdown_html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w') as file:
        file.write(new_page)
    

def main():
    prepare_directory("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()