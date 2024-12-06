import os

def get_template_content(file_name, folder_name=None):
    """
    Returns the content of a template file based on the file name and optional folder name.
    This function loads template files from the 'templates' directory, including any folder structure.
    
    :param file_name: The name of the template file (e.g., 'index.html.text').
    :param folder_name: Optional folder name within 'templates' (e.g., 'css', 'js', or None).
    :return: Content of the template file.
    """
    # Get the base directory of the 'templates' folder
    templates_folder = os.path.dirname(__file__)  # Directory of __init__.py
    
    # Construct the template file path
    if folder_name:
        # If folder_name is provided, look in that subfolder within 'templates'
        template_path = os.path.join(templates_folder, folder_name, f"{file_name}.text")
    else:
        # Otherwise, look directly in 'templates' folder
        template_path = os.path.join(templates_folder, f"{file_name}.text")
    
    # Read and return the template content
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file '{file_name}.text' not found in the 'templates/' directory.")
