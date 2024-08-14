# This Python file uses the following encoding: utf-8
from League import League

from PySide6.QtWidgets import QListWidgetItem

class LeagueWidget(QListWidgetItem):
    league = None

    def __init__(self, league, listWidget):
        super().__init__(league.name, listWidget, 1000)
        self.league = league


