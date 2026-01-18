# MKOcr

A simple OCR pipeline for converting PDFs to searchable PDFs using the Tesseract OCR engine. Available as both a command-line tool and a GUI application built with PyQt6.

## Features

- 📄 Convert scanned PDFs to searchable PDFs
- 🌍 Support for 100+ languages
- 🖼️ Automatic image preprocessing for better OCR accuracy
- 🎨 Modern GUI interface (PyQt6)
- ⚙️ Configurable DPI settings
- 🔧 Command-line interface for batch processing

## Requirements

- Python 3.x
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd MKOcr
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki) or use the default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - **Linux**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`

## Usage

### Command Line Interface

Basic usage:
```bash
python mkocr.py input.pdf output_directory
```

With custom options:
```bash
python mkocr.py input.pdf output_directory --language eng --dpi 450 --tesseract_path "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

**Arguments:**
- `input_path`: Path to the input PDF file
- `output_path`: Directory where the output PDF will be saved
- `--language`: Language code (default: `eng`)
- `--dpi`: DPI value for image extraction (default: `450`)
- `--tesseract_path`: Path to tesseract.exe (Windows default: `C:\Program Files\Tesseract-OCR\tesseract.exe`)

### GUI Application

Launch the graphical interface:
```bash
python mkocr_gui.py
```

## Supported Languages

The tool supports 100+ languages including English, Spanish, French, German, Chinese, Japanese, Arabic, and many more. See `const.py` for the complete list of supported languages and their codes.

## How It Works

1. Opens the input PDF file
2. Converts each page to an image at the specified DPI
3. Performs OCR using Tesseract
4. Creates a searchable PDF with embedded text layers
5. Saves the output to the specified directory

## License

MIT