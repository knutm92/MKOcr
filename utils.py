import os
def create_dir(dir_path: str):
    output_dir = os.path.dirname(dir_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)