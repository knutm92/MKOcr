import os


def create_dir(dir_path: str):
    output_dir = os.path.dirname(dir_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

def get_input_filename(path:str):
    return os.path.basename(path).rsplit('.', 1)[0]

def get_output_filename(path: str):
    input_filename = os.path.basename(path)
    filename_split = input_filename.rsplit('.', 1)
    return f'{filename_split[0]}_ocr.{filename_split[1]}' if len(
        filename_split) > 1 else f'{input_filename}_ocr'
