import os

def data_directory_path():
    """
    This function determine absolute path to data directory
    :return: absolute path to data directory
    """
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Find the project root directory (assuming this script is inside SayNoMore or its subdirectories)
    project_root = current_dir
    while os.path.basename(project_root) != 'SayNoMore':
        project_root = os.path.dirname(project_root)

    # Construct the path to the data directory
    data_directory = os.path.join(project_root, 'data')

    # Ensure the data directory exists
    os.makedirs(data_directory, exist_ok=True)

    return data_directory