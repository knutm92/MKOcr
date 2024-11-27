import pymupdf
import pytesseract
import argparse
import os
import cv2
##TODO: only the last page is saved to pdf
##TODO: add error handling
##TODO: refactor into modules
##TODO: add preprocessing module
##TODO: add some cool """ description


input_path = './sample_data/input/synod_small.pdf'
#output_path =  './sample_data/output'
page_image_dpi = 600
pdf_name = 'synod_small'
tbd_page_image_path = './sample_data_output.synod_small_page_1_.png'

# initialize OCR engine


def mk_ocr(output_path: str, input_path: str = './sample_data/input/synod_small.pdf',  language: str = 'eng', dpi: int = 1200):
    # Set Tesseract engine path
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Open pdf
    pdf = pymupdf.open(input_path)
    print("pdf opened")

    page_pdfs = []
    # Convert pdf to searchable pdf
    for page in pdf:
        page_image = page.get_pixmap(dpi = dpi) #convert pdf page to img
        image_path = f'{output_path}{pdf_name}_page_{page.number}.png'
        page_image.save(image_path) #save img
        print(image_path)

        image = cv2.imread(image_path)

        page_pdf = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang=language, config='pdf') #do OCR
        page_pdfs.append(page_pdf)

    # save searchable pdf to disk
    with open(output_path+'/output.pdf', 'wb') as combined_pdf:
        for page_pdf in page_pdfs:
            combined_pdf.write(page_pdf)


def main():
    # Specify CLI arguments
    parser=argparse.ArgumentParser(description='A simple OCR pipeline for converting pdfs to searchable pdfs using Tesseract OCR engine.')
    parser.add_argument('output_path', help = 'Path to the output file.')
    parser.add_argument('--input_path', default = './sample_data/input/synod_small.pdf', help = 'Path to the input pdf file.')
    parser.add_argument('--language', default = 'eng', help = 'Language of the text.')
    parser.add_argument('--dpi', default = 1200, help = 'DPI value for image extraction. Higher can yield better results, but takes more space disk')

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