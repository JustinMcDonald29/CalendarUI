# This Python file uses the following encoding: utf-8
class Game:
    team_a = None
    team_b = None
    week = None
    avail_times = None
    time = None
    league_set = None

    def __init__(self, a, b):
        self.team_a = a
        self.team_b = b
        self.avail_times = dict()
        if a.league is b.league:
            self.league_set = a.league.time_slots
        else:
            self.league_set = self.merge_league()
        self.set_avail_times()


    def gprint(self, flag):
        if flag:
            print('Week ',self.week, 'matchup')

        print(self.team_a.name,"   vs.   ", self.team_b.name)

    def set_week(self, week):
        self.week = week

    def get_week(self):
        return self.week.copy()

    def get_time(self):
        return self.time.copy()

    def confirm_game(self):
        self.team_a.played_against(self.team_b)
        self.team_b.played_against(self.team_a)

    def merge_league(self):
        working_dict = dict()
        working_set = set()
        for key in ['Sun','Mon','Tues','Wed','Thurs','Fri','Sat']:
            if key in self.team_a.time_blocks and key in self.team_b.time_blocks:
                working_set = self.team_a.time_blocks[key] & self.team_b.time_blocks[key]
            """elif key in self.team_a.time_blocks:
                working_set = self.team_a.time_blocks[key]
            elif key in self.team_b.time_blocks:
                working_set = self.team_b.time_blocks[key]"""
            working_dict.update({key: working_set})
        return working_dict

    def set_avail_times(self):
        self.avail_times = dict()
        working_set = set()
        for key in self.league_set:
            if key in self.team_a.time_blocks and key in self.team_b.time_blocks:
                working_set = self.league_set[key] - (self.team_a.time_blocks[key] | self.team_b.time_blocks[key])
            elif key in self.team_a.time_blocks:
                working_set = self.league_set[key] - self.team_a.time_blocks[key]
            elif key in self.team_b.time_blocks:
                working_set = self.league_set[key] - self.team_b.time_blocks[key]
            else:
                working_set = self.league_set[key]
            self.avail_times.update({key : working_set})
