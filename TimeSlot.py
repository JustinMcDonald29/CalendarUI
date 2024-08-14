# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import (QFont,QColor)
from PySide6.QtCore import (QDateTime, QDate, QTime, Qt)

class TimeSlot(QDateTime):

    def __init__(self, text):
        super().__init__()
