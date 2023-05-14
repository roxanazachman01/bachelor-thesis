from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QDoubleSpinBox


class TimestepWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # self.label = QLabel("\u0394t", self)
        self.label = QLabel("dt", self)
        self.float_picker = QDoubleSpinBox(self)
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        self.float_picker.setLocale(locale)
        self.float_picker.setDecimals(3)
        self.float_picker.setValue(0.05)
        self.float_picker.setMinimum(0)
        self.float_picker.setSingleStep(0.001)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.float_picker, alignment=Qt.AlignRight)

    def get(self):
        return self.float_picker.value()
