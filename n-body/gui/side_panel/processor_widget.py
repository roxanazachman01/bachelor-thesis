import torch.cuda
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

from gui.style.dropdown_delegate import DropdownDelegate
from utils.constants import Processor


class ProcessorWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.processor_dropdown = QComboBox()
        self.processor_dropdown.addItem(Processor.CPU.value, userData=Processor.CPU)
        if torch.cuda.is_available():
            self.processor_dropdown.addItem(Processor.GPU.value, userData=Processor.GPU)
        self.processor_dropdown.setItemDelegate(DropdownDelegate())

        self.layout.addWidget(QLabel("Choose processor:"), alignment=Qt.AlignTop)
        self.layout.addWidget(self.processor_dropdown, alignment=Qt.AlignTop)

    def get(self):
        return self.processor_dropdown.currentData().value
