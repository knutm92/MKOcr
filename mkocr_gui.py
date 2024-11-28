import sys
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, \
    QApplication
from PyQt6.QtCore import pyqtSignal

from mkocr import mk_ocr
import const


class OCRGui(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MKOcr Pipeline')
        self.setGeometry(100, 100, 400, 300)

        # Input for pdf path
        self.input_label = QLabel('Input pdf path:')
        self.input_path = QLineEdit()
        self.input_browse = QPushButton('Browse')
        self.input_browse.clicked.connect(self.browse_input)

        # Run OCR button
        self.run_button = QPushButton('Run OCR!')
        self.run_button.clicked.connect(self.run_ocr)

        # Add created items to the gui box
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(self.input_browse)
        input_layout.addWidget(self.run_button)

        self.setLayout(input_layout)
        print(self.input_label.isVisible())
        print(self.input_path.isVisible())
        print(self.input_browse.isVisible())



    def browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select input pdf', '', 'pdf files (*.pdf);; All Files (*)')
        if file_path:
            self.input_path.setText(file_path)

    def run_ocr(self):
        input_path = self.input_path.text().strip()

        if not input_path or not os.path.isfile(input_path):
            QMessageBox.warning(self, "Input Error", "Invalid input PDF path.")
            return

        try:
            mk_ocr(input_path)
            QMessageBox.information(self, "Success", "OCR completed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OCRGui()
    window.show()
    sys.exit(app.exec())
