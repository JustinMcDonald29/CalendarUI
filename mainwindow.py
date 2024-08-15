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


    def loadUiWidget(self):
        loader = QUiLoader()
        uifile = QFile("SeasonScheduler.ui")
        uifile.open(QFile.ReadOnly)
        self.ui = loader.load(uifile, self)
        uifile.close()

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
    w = MainWin()
    sys.exit(app.exec())



    """class Calendar(QCalendarWidget):
        def __init__(self, parent=None):
            super(Calendar, self).__init__(parent)
            self.verticalHeaderFormat(None)


    class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.initUI()

        def initUI(self):
            self.left = 0
            self.top = 0
            self.width = 600
            self.height = 600
            self.cal = QCalendarWidget( self )
            format = QTextCharFormat()
            #self.setWindowFlags(Qt.FramelessWindowHint)
            self.setGeometry(self.left, self.top, self.width, self.height)
            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.white)
            self.setPalette(p)
            qdim = "QPushButton {color: rgba(54,136,200,250); background-color: black; }"
            canda_10 = QFont("Candalara", 10)
            canda_11 = QFont("Candalara", 11)
            segoe_9 = QFont('Segoe UI', 9)
            format = self.cal.weekdayTextFormat( Qt.Saturday)
            format.setForeground(QBrush(Qt.darkCyan, Qt.SolidPattern))
            self.cal.setWeekdayTextFormat(Qt.Saturday, format)
            self.cal.setWeekdayTextFormat(Qt.Sunday, format)
            self.cal.setVerticalHeaderFormat(self.cal.VerticalHeaderFormat.NoVerticalHeader)
            self.cal.setGridVisible(True)
            self.cal.setGeometry(0,0,300,300)
            self.cal.setFont(segoe_9)
            self.cal.setStyleSheet(
                "QCalendarWidget QAbstractItemView{background-color: lightGray;  color: rgba(162,201,229,255); selection-background-color: rgb(20,20,20); selection-color: rgb(200,150,255); selection-border: 1px solid black;}"
                "QCalendarWidget QWidget{alternate-background-color: rgb(20, 20, 20); color: gray;}"
                "QCalendarWidget QToolButton{background-color: black; color: white; font-size: 14px; font: bold; width: 70px; border: none;}"
                "QCalendarWidget QToolButton#qt_calendar_prevmonth{qproperty-icon: url(left_arrow.png);}"
                "QCalendarWidget QToolButton#qt_calendar_nextmonth{qproperty-icon: url(right_arrow.png);}"
            )
            self.button = QPushButton(self)
            self.button.setStyleSheet(qdim)
            self.button.setFont(canda_11)
            self.button.setText("EXIT")
            self.button.setGeometry(255, 510, 90, 90)
            self.button.clicked.connect(self.exit)
            self.cal.clicked[QDate].connect(self.showDate)

        def showDate(self, date):
            select_date = self.cal.selectedDate()
            string_date = date.toString()
            print(string_date)

        def exit(self):
            self.close()

        def league_window(self):"""






