import copy
class LeagueGroup:

    leagues = None
    week_days = None
    av_games_hold = None
    

    def __init__(self, week_day, league):
        self.week_days = set(week_day)
        self.leagues = set(league)
        self.av_games_hold = dict()

    def merge_week_days(self, week_days):
        self.week_days = set(self.week_days) | set(week_days)

    def add_league(self, league):
        if len(set(league.time_slots.keys()) & self.week_days) < 1 or league.in_group:
            return False
        else:
            self.leagues.add(league)
            self.merge_week_days(league.time_slots.keys())
            league.in_group = True
    
    def hold_add(self, key, item):
        pass
        #self.av_games_hold.update({key: item})

    def get_av_games(self, day, time):
        #av_games = copy.deepcopy(self.av_games_hold)
        out = set()
        for league in self.leagues:
           out = out | league.get_av_games(day, time)
        return out



