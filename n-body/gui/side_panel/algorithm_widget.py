from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

from gui.style.dropdown_delegate import DropdownDelegate
from utils.constants import Algorithm


class AlgorithmWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.algorithm_dropdown = QComboBox()
        for algorithm in Algorithm.__members__.values():
            self.algorithm_dropdown.addItem(algorithm.value[1], userData=algorithm)
        self.algorithm_dropdown.setItemDelegate(DropdownDelegate())

        self.layout.addWidget(QLabel("Choose algorithm:"), alignment=Qt.AlignTop)
        self.layout.addWidget(self.algorithm_dropdown, alignment=Qt.AlignTop)

    def get(self):
        return self.algorithm_dropdown.currentData().value[0]
