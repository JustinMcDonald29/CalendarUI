# This Python file uses the following encoding: utf-8


class Season:
    season = None

    def __init__(self):
        self.season = list()

    def add_week(self, week):
        for game in week.games:
            game.confirm_game()

    def print_season(self):
        for week in self.season:
            week.print_week()

    def reset_season(self):
        self.season = list()

