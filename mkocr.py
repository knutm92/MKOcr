import const
from argument_parser import parse_arguments
from postprocessing import pdf_append, remove_image
from preprocessing import open_pdf, pdf_to_img
from processing import run_tesseract
from utils import create_dir, get_output_filename, get_input_filename


##TODO: add error handling
##TODO: improve prints (ocr of page 1... done)
##TODO: refactor into modules
##TODO: add some cool """ description
##TODO: remove img after the ocr process


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

    def do_ocr(self):
        pdf_name = get_input_filename(path=self.input_path)
        output_filename = get_output_filename(path=self.input_path)
        # Open pdf
        try:
            pdf = open_pdf(self.input_path)
        except RuntimeError as error:
            print(error)
            print('OCR processing terminated')
            exit()

        # Initialize output pdf file
        output_pdf = None

        # Convert pdf to searchable pdf
        for page in pdf:
            # Convert pdf page to img
            image_path = pdf_to_img(dpi=self.dpi, pdf_name=pdf_name, output_path=self.output_path, page=page)

            print(f'Doing OCR of page {page.number}...', end=' ')
            # Perform OCR
            processed_page = run_tesseract(image_path=image_path, language=self.language,
                                           tesseract_path=self.tesseract_path)
            print('Done')
            remove_image(image_path)
            # Append the current page to the searchable pdf
            output_pdf = pdf_append(processed_page, output_pdf)

        print(f'Saving {self.output_path}/{output_filename}')
        output_pdf.save(self.output_path + f'/{output_filename}')  # Compact object stream


def main():
    # Parse arguments
    args = parse_arguments()

    # Create output dir if it does not exist
    create_dir(args.output_path)

    # Run the pipeline
    processor = MkOcr(input_path=args.input_path, output_path=args.output_path, tesseract_path=args.tesseract_path,
                      language=args.language,
                      dpi=args.dpi)
    processor.do_ocr()


if __name__ == "__main__":
    main()
