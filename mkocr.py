import pymupdf
import pytesseract
import argparse
import os
import cv2
import pikepdf
import io

##TODO: add error handling
##TODO: refactor into modules
##TODO: add preprocessing module
##TODO: add some cool """ description


pdf_name = 'synod_small'
tbd_page_image_path = './sample_data_output.synod_small_page_1_.png'
default_dpi = 450

# initialize OCR engine


def mk_ocr(output_path: str, input_path: str = './sample_data/input/synod_small.pdf', language: str = 'eng',
           dpi: int = default_dpi):
    # Set Tesseract engine path
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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

        # Open the page image
        image = cv2.imread(image_path)
        print("doing ocr")

        # Perform OCR
        page_pdf = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang=language, config='pdf')  # do OCR
        print("ocr done")

        # Save to pdf
        page = pikepdf.Pdf.open(io.BytesIO(page_pdf))
        pdf_file.pages.extend(page.pages)
    print(f"trying to save {output_path}./output.pdf")
    pdf_file.save(output_path + '/output.pdf')  # Compact object stream

    """page_pdfs.append(page_pdf)

    # save searchable pdf to disk
    with open(output_path+'/output.pdf', 'wb') as combined_pdf:
        for page_pdf in page_pdfs:
            combined_pdf.write(page_pdf)"""


def main():
    # Specify CLI arguments
    parser = argparse.ArgumentParser(
        description='A simple OCR pipeline for converting pdfs to searchable pdfs using Tesseract OCR engine.')
    parser.add_argument('output_path', help='Path to the output file.')
    parser.add_argument('--input_path', default='./sample_data/input/synod_small.pdf',
                        help='Path to the input pdf file.')
    parser.add_argument('--language', default='eng', help='Language of the text.')
    parser.add_argument('--dpi', default=default_dpi,
                        help='DPI value for image extraction. Higher can yield better results, but takes more space disk')

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
