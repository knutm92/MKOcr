import pytesseract
import cv2

def run_tesseract(image_path: str, language: str, tesseract_path: str):
    # Open image
    image = cv2.imread(image_path)

    # Set Tesseract engine path
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    # Run ocr from image to pdf
    return pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang=language,
                                            config='pdf')
