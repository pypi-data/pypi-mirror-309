import os
import json
import logging
import pkg_resources

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_template_content(template_name, folder=None):
    """
    Get the content of a template file from the templates directory.
    
    :param template_name: Name of the template file (e.g., 'index.html.text')
    :param folder: The folder name (used if templates are organized by folder)
    :return: Content of the template file
    """
    if folder:
        template_path = pkg_resources.resource_filename('spike_webx', f'templates/{folder}/{template_name}')
    else:
        template_path = pkg_resources.resource_filename('spike_webx', f'templates/{template_name}')
    
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"Template file {template_name} not found in templates.")
        return ""

def create_structure_from_json(base_path, json_file):
    """
    Create a folder structure and populate files using predefined templates from a JSON definition.
    
    :param base_path: The base directory where the structure will be created
    :param json_file: Path to the JSON file defining the structure
    """
    # Load the structure definition from JSON
    try:
        with open(json_file, 'r') as f:
            structure = json.load(f)
    except FileNotFoundError:
        logging.error(f"JSON file {json_file} not found.")
        return
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the file {json_file}.")
        return
    
    root_folder = os.path.join(base_path, structure.get("name", "default_project"))
    
    # Create the root folder
    try:
        os.makedirs(root_folder, exist_ok=True)
        logging.info(f"Created root folder: {root_folder}")
    except PermissionError:
        logging.error(f"Permission denied to create folder {root_folder}.")
        return
    
    # Create the files in the root folder (e.g., index.html)
    for file in structure.get("files", []):
        file_path = os.path.join(root_folder, file)
        try:
            content = get_template_content(file)  # Get template content for root files
            with open(file_path, 'w') as f:
                f.write(content)
            logging.info(f"Created file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to create file {file_path}: {e}")
    
    # Create subfolders and their files
    for folder in structure.get("folders", []):
        folder_path = os.path.join(root_folder, folder["name"])
        try:
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f"Created folder: {folder_path}")
        except PermissionError:
            logging.error(f"Permission denied to create folder {folder_path}.")
            continue
        
        for file in folder.get("files", []):
            file_path = os.path.join(folder_path, file)
            try:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):  # Check if it's an image file
                    # Copy the image from the templates folder to the assets folder
                    image_path = os.path.join("templates", file)  # Adjust this path if necessary
                    with open(image_path, 'rb') as img_file:
                        content = img_file.read()
                    with open(file_path, 'wb') as f:
                        f.write(content)
                    logging.info(f"Created image file: {file_path}")
                else:
                    # For non-image files, use the template content
                    content = get_template_content(file, folder["name"])
                    with open(file_path, 'w') as f:
                        f.write(content)
                    logging.info(f"Created file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to create file {file_path}: {e}")

if __name__ == "__main__":
    # Define base path and the JSON structure file
    base_path = "./spikeset_project"
    json_file = "templates/folder_structure.json"
    create_structure_from_json(base_path, json_file)
