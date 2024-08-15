# This Python file uses the following encoding: utf-8
import sys, os
from datetime import datetime
from League import League
from Week import Week
from Game import Game
from Team import Team


from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QTextEdit,
    QTableWidget,
    QWidget,
    QPushButton,
    QCalendarWidget,
    QTableWidgetItem,
    QListWidgetItem,
)

from LeagueWidget import LeagueWidget
from TeamWidget import TeamWidget
from PySide6.QtCore import QDate, Qt, QRect, QIODevice, QFile
from PySide6.QtUiTools import QUiLoader

from PySide6.QtGui import(
    QFont,
    QColor,
    QBrush,
    QPainter,
    QTextCharFormat,
)

class MainWin(QMainWindow):
    leagues = {}
    active_league = None
    league_start_flag = False

    def __init__(self):
        super().__init__()
        self.loadUiWidget()
        self.connector()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.show()
        self.ui.weekScheduleButton.setHidden(True)
        self.ui.weekScheduleButton.setEnabled(False)
        self.ui.setFixedSize(1136, 770)  # Example dimensions, adjust as neede
        print(self.window)
    
    def loadUiWidget(self):
        loader = QUiLoader()
        uifile = QFile("SeasonScheduler.ui")
        uifile.open(QFile.ReadOnly)
        self.ui = loader.load(uifile, self)
        uifile.close()

        # Set the central widget of the main window to the loaded UI
        self.setCentralWidget(self.ui)

    def closeEvent(self, event):
       # event.accept()  # Accept the event to close the windo  # Close the window
        QApplication.quit()  # Quit the application

    def connector(self):
        self.ui.homeButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.leaguesButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.weekScheduleButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.createLeagueButton.clicked.connect(self.ui.createLeagueLine.editingFinished)
        self.ui.createLeagueLine.editingFinished.connect(self.add_league)
        self.ui.addTeamButton.clicked.connect(self.ui.addTeamLine.editingFinished)
        self.ui.addTeamLine.editingFinished.connect(self.add_team)
        self.ui.leagueListWidget.itemClicked.connect(self.set_active_league)
        self.ui.stackedWidget.currentChanged.connect(self.stacked_logic)
        self.ui.leagueDateButton.clicked.connect(self.set_leagueDate)
        self.ui.teamListWidget.itemSelectionChanged.connect(self.teams_logic)
        self.ui.timeBlockButton.clicked.connect(self.set_timeBlock)
        self.ui.matchupsButton.clicked.connect(self.ui.matchupsLine.editingFinished)
        self.ui.matchupsLine.editingFinished.connect(self.gen_league_matchups)
        self.ui.leagueStartButton.clicked.connect(self.set_league_start)
        self.ui.calendarWidget.clicked[QDate].connect(self.calendar_logic)

    def add_league(self):
        if not self.ui.createLeagueLine.isModified():
            return
        league = League(self.ui.createLeagueLine.text())
        #print(id(league))
        self.ui.createLeagueLine.setText('')
        item = LeagueWidget(league, self.ui.leagueListWidget)
        #print("league created, name: ", league.name)
        self.leagues.update({league.name: league})
        self.set_active_league(item)

    def set_active_league(self, clickedItem):

        self.active_league = None
        self.active_league = clickedItem.league
        self.ui.stackedWidget.setCurrentIndex(2)
        self.gen_league_mgmt()

    def add_team(self):
        if not self.ui.addTeamLine.isModified():
            return
        self.active_league.add_team(self.ui.addTeamLine.text())
        self.ui.addTeamLine.setText('')

        self.gen_league_mgmt()

    def gen_league_matchups(self):
        try:
            text = int(self.ui.matchupsLine.text())
            self.active_league.gen_season(text)
        except:
            print("Naughty boy don't put letters in there")
        if not self.ui.matchupsLine.isModified():
            return

        self.ui.matchupsLine.setText('')


    def set_leagueDate(self):
        out = dict()
        for col in range(self.ui.leagueDateTable.columnCount()):
            header = self.ui.leagueDateTable.horizontalHeaderItem(col)
            h_text = str(header.text())
            flag = False
            working_set = set()
            for row in range(self.ui.leagueDateTable.rowCount()):
                item = self.ui.leagueDateTable.item(row, col)                
                if type(item) is QTableWidgetItem:
                    text = item.text()
                    if item.checkState() == Qt.Checked:
                        working_set.add(text)
                        flag = True
            if flag:
                out.update({h_text:working_set})
        self.active_league.set_time_slots(out)

    def set_timeBlock(self):
        out = dict()
        for col in range(self.ui.timeBlockTable.columnCount()):
            header = self.ui.timeBlockTable.horizontalHeaderItem(col)
            h_text = str(header.text())
            flag = False
            working_set = set()
            for row in range(self.ui.timeBlockTable.rowCount()):
                item = self.ui.timeBlockTable.item(row, col)
                if type(item) is QTableWidgetItem:
                    text = item.text()
                    if item.checkState() == Qt.Checked:
                        working_set.add(text)
                        flag = True
            if flag:
                out.update({h_text:working_set})
        self.ui.teamListWidget.currentItem().team.set_time_blocks(out)


    def stacked_logic(self):
        if self.ui.stackedWidget.currentIndex() == 2:
            self.gen_league_mgmt()
            self.ui.league_tab.setCurrentIndex(0)
            self.ui.leagueLable.setText(self.active_league.name)

        if self.active_league is not None:
            self.ui.weekScheduleButton.setEnabled(True)
            self.ui.weekScheduleButton.setHidden(False)

        if self.ui.stackedWidget.currentIndex() != 0:
            self.league_start_flag = False

    def teams_logic(self):
        self.ui.league_tab.setCurrentIndex(1)
        self.ui.weekBlockLable.setText(self.ui.teamListWidget.currentItem().text())
        self.gen_timeBlockTable()

    def calendar_logic(self, date):
        if self.league_start_flag:
            self.active_league.set_start_date(self.ui.calendarWidget.selectedDate())
            self.league_start_flag = False


    def set_league_start(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.league_start_flag = True


    def gen_league_mgmt(self):
        self.ui.teamListWidget.clear()
        if self.active_league is not None:
            for team in self.active_league.teams:
                item = TeamWidget(self.active_league.teams[team], self.ui.teamListWidget)
            self.gen_leagueDateTable()

    def gen_leagueDateTable(self):
        for col in range(self.ui.leagueDateTable.columnCount()):
            header = self.ui.leagueDateTable.horizontalHeaderItem(col)
            for i in range(6,11):
                if header.text() == "Fri" or header.text() == 'Mon':
                    timestring = str(i)+":30"
                    if i == 10:
                        break
                else:
                    timestring = str(i)+":00"
                item = QTableWidgetItem(timestring)
                if self.active_league.time_slots:
                    if item.text() in self.active_league.time_slots[header.text()]:
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Unchecked)
                self.ui.leagueDateTable.setItem(i-6,col,item)

    def gen_timeBlockTable(self):
        for col in range(self.ui.timeBlockTable.columnCount()):
            header = self.ui.timeBlockTable.horizontalHeaderItem(col)
            for i in range(6,11):
                if header.text() == "Fri" or header.text() == 'Mon':
                    timestring = str(i)+":30"
                    if i == 10:
                        break
                else:
                    timestring = str(i)+":00"
                item = QTableWidgetItem(timestring)
                if self.ui.teamListWidget.currentItem().team.time_blocks:
                    if item.text() in self.ui.teamListWidget.currentItem().team.time_blocks[header.text()]:
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Unchecked)
                self.ui.timeBlockTable.setItem(i-6,col,item)








if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    #QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    w = MainWin()
    w.show()
    sys.exit(app.exec())