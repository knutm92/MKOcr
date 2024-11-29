import pymupdf
import pytesseract
import argparse
import os
import cv2
import pikepdf
import io
import const
import PyQt6

##TODO: add error handling
##TODO: refactor into modules
##TODO: add some cool """ description


pdf_name = 'synod_small'


# initialize OCR engine

def remove_noise(image):
    denoised = cv2.medianBlur(image, const.noise_kernel)  # Adjust kernel size as needed
    return denoised


def apply_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, const.threshold_block, const.threshold_c)

    return binary


def mk_ocr(output_path: str, input_path: str, language: str = 'eng',
           dpi: int = const.default_dpi, tesseract_path: str = const.default_tesseract_path):
    # Set Tesseract engine path
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    # Create output filename
    input_filename = os.path.basename(input_path)
    filename_split = input_filename.rsplit('.', 1)
    output_filename = f'{filename_split[0]}_ocr.{filename_split[1]}' if len(filename_split) > 1 else f'{input_filename}_ocr'

    # Open pdf
    pdf = pymupdf.open(input_path)
    print("pdf opened")

    pdf_file = pikepdf.Pdf.new()
    # Convert pdf to searchable pdf
    for page in pdf:
        # Convert pdf page to img
        page_image = page.get_pixmap(dpi=dpi)

        # Save img to a file
        image_path = f'{output_path}{pdf_name}_page_{page.number}.png'
        page_image.save(image_path)  # save img
        print(image_path)

        # Save morphed image for comparison
        image_path_hq = f'{output_path}{pdf_name}_page_{page.number}_hq.png'

        # these are quality improvements:
        page_image_hq = apply_threshold(cv2.imread(image_path))

        cv2.imwrite(image_path_hq, page_image_hq)  # save img
        print(image_path_hq)

        # Open the page image
        image = cv2.imread(image_path)
        print("doing ocr")

        # Perform OCR
        page_pdf = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang=language, config='pdf')  # do OCR
        print("ocr done")

        # Save to pdf
        page = pikepdf.Pdf.open(io.BytesIO(page_pdf))
        pdf_file.pages.extend(page.pages)
    print(f"trying to save {output_path}/{output_filename}")
    pdf_file.save(output_path + f'/{output_filename}')  # Compact object stream


def main():
    # Specify CLI arguments
    parser = argparse.ArgumentParser(
        description='A simple OCR pipeline for converting pdfs to searchable pdfs using Tesseract OCR engine.')
    parser.add_argument('output_path', help='Path to the output file.')
    parser.add_argument('input_path',
                        help='Path to the input pdf file.')
    parser.add_argument('--language', default='eng', help='Language of the text.')
    parser.add_argument('--dpi', default=const.default_dpi,
                        help='DPI value for image extraction. Higher can yield better results, but takes more space disk')
    parser.add_argument('--tesseract_path', default=r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                        help='Path to tesseract.exe,')

    # Parse arguments
    args = parser.parse_args()

    # Create output dir if it does not exist
    output_dir = os.path.dirname(args.output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run mkocr pipeline

    mk_ocr(args.output_path, args.input_path, args.language, args.dpi)


if __name__ == "__main__":
    main()
