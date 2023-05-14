from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle


class DropdownDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if option.state & QStyle.State_MouseOver:
            bg_color = QColor("#303040")
        elif option.state & QStyle.State_Selected:
            bg_color = QColor("#303045")
        else:
            bg_color = QColor("#252535")
        painter.fillRect(option.rect, QBrush(bg_color))
        painter.setPen(Qt.white)
        painter.drawText(option.rect, Qt.AlignCenter, index.data(Qt.DisplayRole))

    def sizeHint(self, option, index):
        text = index.data()
        fontMetrics = option.fontMetrics
        textSize = fontMetrics.size(Qt.TextSingleLine, text)
        width = textSize.width() + 10
        height = textSize.height() + 10
        return QSize(width, height)
