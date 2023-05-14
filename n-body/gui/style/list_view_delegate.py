from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import QBrush, QColor, QFont, QPainterPath, QPainter
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle


class ListViewDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        bg_color = QColor("#303040")
        if option.state & QStyle.State_MouseOver:
            bg_color = QColor("#353550")
        elif option.state & QStyle.State_Selected:
            bg_color = QColor("#353555")
        painter.fillRect(option.rect, QBrush(bg_color))

        # painter.setRenderHint(QPainter.Antialiasing)  # enable antialiasing to make the rounded corners smoother
        # painter.setBrush(QBrush(bg_color))
        # painter.setPen(Qt.NoPen)
        # painter.drawRoundedRect(option.rect, 25, 25)

        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(option.rect, Qt.AlignCenter, index.data())

    # def sizeHint(self, option, index):
    #     text = index.data()
    #     fontMetrics = option.fontMetrics
    #     textSize = fontMetrics.size(Qt.TextSingleLine, text)
    #     width = textSize.width() + 20  # add some extra space for padding
    #     height = textSize.height() + 10
    #     return QSize(width, height)
