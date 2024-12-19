import io
import pikepdf
import os

def remove_image(image_path: str):
    os.remove(image_path)

def pdf_append(pdf_page, pdf_file = None):
    if pdf_file is None:
        pdf_file = pikepdf.Pdf.new()
    page = pikepdf.Pdf.open(io.BytesIO(pdf_page))
    pdf_file.pages.extend(page.pages)
    return pdf_file