# This Python file uses the following encoding: utf-8


class Season:
    season = None

    def __init__(self):
        self.season = list()
        #print("season initialized")

    def add_week(self, week):
        for game in week.games:
            game.confirm_game()
        self.season.append(week)
        week.print_week()
        #print("week added")
        print(self.season)
        

    def print_season(self):
        print("Printing Season:")
        for week in self.season:
            week.print_week()

    def reset_season(self):
        self.season = list()

    def get_week(self, week_num):
        return self.season[week_num]

    def get_games(self, week_num):
        return self.season[week_num].get_games()