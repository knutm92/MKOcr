import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, \
    QApplication, QSlider, QComboBox

import const
from mkocr import MkOcr

class OCRGui(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.lang_code = const.default_language_code

    def init_ui(self):
        self.setWindowTitle('MKOcr Pipeline')
        self.setGeometry(100, 100, 400, 300)

        # Tesseract path
        self.tesseract_label = QLabel('Tesseract.exe path:')
        self.tesseract_path = QLineEdit()
        self.tesseract_path.setText(const.default_tesseract_path)
        self.tesseract_browse = QPushButton('Browse')
        self.tesseract_browse.clicked.connect(self.browse_input)

        # Input for pdf path
        self.input_label = QLabel('Input pdf path:')
        self.input_path = QLineEdit()
        self.input_browse = QPushButton('Browse')
        self.input_browse.clicked.connect(self.browse_input)

        # Output path
        self.output_label = QLabel('Output dir path:')
        self.output_path = QLineEdit()
        self.output_browse = QPushButton('Browse')
        self.output_browse.clicked.connect(self.browse_output)

        # DPI
        self.dpi_label = QLabel('DPI: 300')
        self.dpi_slider = QSlider(Qt.Orientation.Horizontal)
        self.dpi_slider.setRange(72, 900)
        self.dpi_slider.setValue(const.default_dpi)
        self.dpi_slider.valueChanged.connect(self.update_dpi)

        # Run OCR button
        self.run_button = QPushButton('Run OCR!')
        self.run_button.clicked.connect(self.run_ocr)

        # Language drop-down list
        self.language_dropdown = QComboBox()
        self.language_label = QLabel('Select text language: ')
        self.language_dropdown.addItems(const.tesseract_languages.keys())
        self.language_dropdown.setCurrentText(const.default_language)
        self.language_dropdown.currentTextChanged.connect(self.update_language)

        # Main Layout
        main_layout = QVBoxLayout()

        # Construct tesseract layout
        tesseract_layout = QHBoxLayout()
        tesseract_layout.addWidget(self.tesseract_label)
        tesseract_layout.addWidget(self.tesseract_path)
        tesseract_layout.addWidget(self.tesseract_browse)

        # Construct output layout
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.output_browse)

        # Construct input layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(self.input_browse)

        # Construct dpi layout
        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(self.dpi_label)
        dpi_layout.addWidget(self.dpi_slider)

        # Construct language layout
        language_layout = QHBoxLayout()
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_dropdown)

        # Construct main layout
        main_layout.addLayout(tesseract_layout)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(dpi_layout)
        main_layout.addLayout(language_layout)

        # Add run button below
        main_layout.addWidget(self.run_button)

        self.setLayout(main_layout)

    def browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select input pdf', '', 'pdf files (*.pdf);; All Files (*)')
        if file_path:
            self.input_path.setText(file_path)

    def browse_output(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select output folder')
        if dir_path:
            self.output_path.setText(dir_path)

    def update_dpi(self):
        dpi_value = self.dpi_slider.value()
        self.dpi_label.setText(f"DPI: {dpi_value}")

    def update_language(self, selected_language):
        self.lang_code = const.tesseract_languages[selected_language]

    def run_ocr(self):
        tesseract_path = self.tesseract_path.text().strip()
        input_path = self.input_path.text().strip()
        output_path = self.output_path.text().strip()
        dpi = self.dpi_slider.value()
        language = self.lang_code

        if not input_path or not os.path.isfile(input_path):
            QMessageBox.warning(self, "Input Error", "Invalid input PDF path.")
            return

        try:
            processor = MkOcr(output_path=output_path, input_path=input_path, dpi=dpi, tesseract_path=tesseract_path,
                   language=language)
            processor.do_ocr()
            QMessageBox.information(self, "Success", "OCR completed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OCRGui()
    window.show()
    sys.exit(app.exec())
