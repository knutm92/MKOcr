import argparse
import const


def parse_arguments():
    # Specify CLI arguments
    parser = argparse.ArgumentParser(
        description='A simple OCR pipeline for converting pdfs to searchable pdfs using Tesseract OCR engine.')
    parser.add_argument('input_path',
                        help='Path to the input pdf file.')
    parser.add_argument('output_path', help='Path to the output file.')
    parser.add_argument('--tesseract_path', default=r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                        help='Path to tesseract.exe,')
    parser.add_argument('--language', default='eng', help='Language of the text.')
    parser.add_argument('--dpi', type=int, default=const.default_dpi,
                        help='DPI value for image extraction. Higher can yield better results, but takes more space disk')
    return parser.parse_args()
