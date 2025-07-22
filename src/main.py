import os, sys
import shutil

from pathlib import Path
from block_markdown import extract_title, markdown_to_html_node


DIR_STATIC = "static"
DIR_DOCS = "docs" # for GitHub Pages deployment
DIR_PUBLIC = "public" # for local deployment
DIR_CONTENT = "content"
TEMPLATE_FILE = "template.html"

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

def generate_page(from_path, template_path, dest_path, basepath=None):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown_file = file.read()

    markdown_html = markdown_to_html_node(markdown_file).to_html()
    page_title = extract_title(markdown_file)

    with open(template_path, 'r') as file:
        template_file = file.read()
    new_page = template_file.replace("{{ Title }}", page_title)
    new_page = new_page.replace("{{ Content }}", markdown_html)

    if basepath:
        new_page = new_page.replace('href="/', f'href="{basepath}')
        new_page = new_page.replace('src="/', f'src="{basepath}')

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w') as file:
        file.write(new_page)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath=None):
    for node in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, node)
        dest_path = os.path.join(dest_dir_path, node)
        if os.path.isfile(source_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(source_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(source_path, template_path, dest_path, basepath)

def main():
    # Usage: python3 src/main.py [local|github] [basepath]
    output_dir = DIR_PUBLIC  # Default to local deployment
    basepath = "/"

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "github":
            output_dir = DIR_DOCS
            print("Deploying for Github.")
        elif arg == "local":
            output_dir = DIR_PUBLIC
            print("Deploying locally.")
        else:
            print(f"Unknown deployment type '{arg}'. Defaulting to local deployment (outputs to '{DIR_PUBLIC}').")
    else:
        print("No deployment type specified. Defaulting to local deployment (outputs to 'public').")

    if len(sys.argv) > 2:
        basepath = sys.argv[2]
        print(f"Using '{basepath}' as the basepath.")
    else:
        print("No basepath specified, defaulting to '/' for the path.")

    prepare_directory(DIR_STATIC, output_dir)
    generate_pages_recursive(DIR_CONTENT, TEMPLATE_FILE, output_dir, basepath)

if __name__ == "__main__":
    main()