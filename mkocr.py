import cv2
import pymupdf

import const
from argument_parser import parse_arguments
from postprocessing import pdf_append
from processing import run_tesseract
from utils import create_dir, get_output_filename

##TODO: add error handling
##TODO: improve prints (ocr of page 1... done)
##TODO: refactor into modules
##TODO: add some cool """ description
##TODO: remove img after the ocr process


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


class MkOcr:
    """
    Handles pdf to image conversion, preprocessing, image ocr and saves the result as a searchable pdf.
    """

    def __init__(self,
                 input_path: str = None,
                 output_path: str = None,
                 tesseract_path: str = None,
                 language: str = const.default_language_code,
                 dpi: int = const.default_dpi
                 ):
        self.input_path = input_path
        self.output_path = output_path
        self.tesseract_path = tesseract_path
        self.language = language
        self.dpi = dpi

    def mk_ocr(self):
        output_filename = get_output_filename(path=self.input_path)

        # Open pdf
        pdf = pymupdf.open(self.input_path)
        print("pdf opened")

        # Initialize pdf file
        pdf_file = None

        # Convert pdf to searchable pdf
        for page in pdf:
            # Convert pdf page to img
            page_image = page.get_pixmap(dpi=self.dpi)

            # Save img to a file
            image_path = f'{self.output_path}{pdf_name}_page_{page.number}.png'
            page_image.save(image_path)  # save img
            print(image_path)

            # Save morphed image for comparison
            image_path_hq = f'{self.output_path}{pdf_name}_page_{page.number}_hq.png'

            # these are quality improvements:
            page_image_hq = apply_threshold(cv2.imread(image_path))

            cv2.imwrite(image_path_hq, page_image_hq)  # save img
            print(image_path_hq)

            print(f'Doing OCR of page {page.number}...', end=' ')
            # Perform OCR
            processed_page = run_tesseract(image_path=image_path, language=self.language,
                                           tesseract_path=self.tesseract_path)
            print('Done')

            # Append the current page to the searchable pdf
            pdf_file = pdf_append(processed_page, pdf_file)

        print(f'Saving {self.output_path}/{output_filename}')
        pdf_file.save(self.output_path + f'/{output_filename}')  # Compact object stream


def main():
    # Parse arguments
    args = parse_arguments()

    # Create output dir if it does not exist
    create_dir(args.output_path)

    # Run mkocr pipeline
    processor = MkOcr(input_path=args.input_path, output_path=args.output_path, tesseract_path=args.tesseract_path,
                      language=args.language,
                      dpi=args.dpi)
    processor.mk_ocr()


if __name__ == "__main__":
    main()
