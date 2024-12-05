import cv2
import pymupdf

import const


def open_pdf(pdf_path: str):
    try:
        pdf = pymupdf.open(pdf_path)
        return pdf
    except Exception as e:
        raise RuntimeError('Failed to open pdf file.')


def remove_noise(image):
    denoised = cv2.medianBlur(image, const.noise_kernel)  # Adjust kernel size as needed
    return denoised


def apply_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, const.threshold_block, const.threshold_c)

    return binary


def pdf_to_img(dpi: int, pdf_name: str, output_path: str, page):
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

    cv2.imwrite(image_path_hq, page_image_hq)
    return image_path
