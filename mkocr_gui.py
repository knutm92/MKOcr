import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, \
    QApplication, QSpinBox, QSlider

import const
from mkocr import mk_ocr


class OCRGui(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        '''
        # Initialize the attributes
        self.input_label = None
        self.input_path = None
        self.input_browse = None
        self.run_button = None'''

    def init_ui(self):
        self.setWindowTitle('MKOcr Pipeline')
        self.setGeometry(100, 100, 400, 300)

        # Input for pdf path
        self.input_label = QLabel('Input pdf path:')
        self.input_path = QLineEdit()
        self.input_browse = QPushButton('Browse')
        self.input_browse.clicked.connect(self.browse_input)

        # Output path
        self.output_label = QLabel('Output path:')
        self.output_path = QLineEdit()
        self.output_browse = QPushButton('Browse')
        self.output_browse.clicked.connect(self.browse_output)
        # DPI
        self.dpi_label = QLabel('DPI:')
        self.dpi_input = QSlider(Qt.Orientation.Horizontal)
        self.dpi_input.setRange(72, 900)
        self.dpi_input.setValue(const.default_dpi)
        # self.dpi_value = QLabel(f'dpi value: {self.dpi_input.value()}')
        # self.dpi_input.valueChanged.connect(self.dpi_value)

        # Run OCR button
        self.run_button = QPushButton('Run OCR!')
        self.run_button.clicked.connect(self.run_ocr)

        # Main Layout
        main_layout = QVBoxLayout()

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
        # TODO: add a slider tag with the selected value
        # TODO: pass selected dpi value to the pipeline
        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(self.dpi_label)
        dpi_layout.addWidget(self.dpi_input)
        # dpi_layout.addWidget(self.dpi_value)

        # spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        # input_layout.addItem(spacer)
        # Construct main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(dpi_layout)

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

    def run_ocr(self):
        input_path = self.input_path.text().strip()
        output_path = self.output_path.text().strip()
        dpi = self.dpi_input.value()

        if not input_path or not os.path.isfile(input_path):
            QMessageBox.warning(self, "Input Error", "Invalid input PDF path.")
            return

        try:
            mk_ocr(output_path=output_path, input_path=input_path, dpi=dpi)
            QMessageBox.information(self, "Success", "OCR completed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OCRGui()
    window.show()
    sys.exit(app.exec())
