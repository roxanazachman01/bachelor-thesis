import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QHBoxLayout, QLabel, QVBoxLayout


class FilePickerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.button = QPushButton('Select input file', self)
        self.button.setIcon(QIcon(os.path.join('gui', 'style', 'upload3.png')))
        self.button.setStyleSheet('padding:5px')
        self.button.setIconSize(self.button.sizeHint())
        self.button.clicked.connect(self.show_dialog)

        self.file_path = os.path.abspath(os.path.join('star_cluster', 'lala', 'n_0.csv'))
        basefile = os.path.basename(self.file_path)
        basefile = basefile if len(basefile) < 12 else basefile[:12] + "..."
        self.selected_file_label = QLabel(f'Selected file: {basefile}')
        self.selected_file_label.setStyleSheet('color:#505060; font-size:13px;')

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.selected_file_label)

    def show_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '.', 'Text files (*.csv)')
        if self.file_path:
            basefile = os.path.basename(self.file_path)
            basefile = basefile if len(basefile) < 12 else basefile[:12] + "..."
            self.selected_file_label.setText(f'Selected file: {basefile}')

    def get(self):
        return self.file_path
