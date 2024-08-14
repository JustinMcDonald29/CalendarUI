# This Python file uses the following encoding: utf-8
import copy

class Team:
    name = None
    games_played = None
    last = None
    tindex = None
    done = False
    time_blocks = None
    league = None

    def __init__(self, name, index, league):
        self.name = name
        self.tindex = index
        print("Team Successfully Created: ", name)
        self.games_played = 0
        self.league = league
    def played_against(self, team):
        self.games_played += 1
        self.last = team.name

    def reset_team(self):
        self.games_played = 0
        self.last = None

    def get_name(self):
        return self.name.copy()

    def set_time_blocks(self, time_blocks):
        self.time_blocks = copy.deepcopy(time_blocks)
        print("setting time blocks")
        print(self.time_blocks)

    def set_name(self, name):
        self.name = name

    def get_games_played(self):
        return self.games_played

    def set_games_played(self, games_played):
        self.games_played = games_played

    def get_last(self):
        return self.last.copy()

    def set_last(self, team):
        self.last = team

    def get_tindex(self):
        return self.tindex.copy()

    def set_tindex(self, tindex):
        self.tindex = tindex

    def get_done(self):
        return self.done

    def set_done(self, done):
        self.done = done

    def set_league(self, league):
        self.league = league

