# This Python file uses the following encoding: utf-8
from Team import Team
from PySide6.QtWidgets import QListWidgetItem

class TeamWidget(QListWidgetItem):
    team = None

    def __init__(self, team, listWidget):
        super().__init__(team.name, listWidget, 1000)
        self.team = team

