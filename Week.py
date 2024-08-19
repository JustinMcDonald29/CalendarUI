# This Python file uses the following encoding: utf-8

import copy

from Game import Game
from Team import Team
import math


class Week:
    games = None
    week = None
    matchup_state = None
    bye = None
    trio_flag = False
    confirm_flag = False
    teams_state = None

    def __init__(self, week):
        self.week = week
        self.games = list()
        self.bye = list()

    def add_game(self, game):
        self.games.append(game)
        game.set_week(self.week)
        #print("games: ",self.games)

    def clear_week(self):
        self.games = []
        self.trio_flag = False
        self.confirm_flag = False
        self.matchup_state = None
        self.teams_state = None

    def print_week(self):
        for g in self.games:
            g.gprint(True)

    def get_size(self):
        return len(self.games)

    def confirm_week(self, true_matchups, max_against, teams):
        matchups = copy.deepcopy(true_matchups)
        self.print_week()

        if len(self.games) < math.floor(len(teams)/2):
            self.confirm_flag = False
            return

        for i in self.games:
            matchups[i.team_a.tindex][i.team_b.tindex] += 1
            matchups[i.team_b.tindex][i.team_a.tindex] += 1
            if len(self.remaining_opps(i.team_a.tindex, matchups, max_against)) == 3 or len(self.remaining_opps(i.team_b.tindex, matchups, max_against)) == 3:

                self.trio_flag = True

        #for i in range(len(matchups[0])):
            #print(matchups[i])
        if self.trio_flag:
            if self.trio_check(matchups, max_against):
                self.confirm_flag = False
                return
        self.matchup_state = matchups
        self.teams_state = teams
        self.confirm_flag = True

        return

    def trio_check(self, matchups, max_against):
        """A "trio" is a condition wherein a trio of teams only have each other remaining as possible opponents,
        the consequence of this being that when a week is generated one will be left out"""
        a_flag = False
        b_flag = False

        # make list of remaining opponents
        for game in self.games:

            a_opps = self.remaining_opps(game.team_a.tindex, matchups, max_against)

            if len(a_opps) == 3 and not a_flag:
                for item in a_opps:

                    if item == game.team_a.tindex:
                        continue
                    item_set = self.remaining_opps(item, matchups, max_against)

                    if (a_opps.issubset(item_set) and item_set.issubset(a_opps)) or len(a_opps.intersection(item_set)) == 0:
                        a_flag = True

            b_opps = self.remaining_opps(game.team_b.tindex, matchups, max_against)

            if len(b_opps) == 3 and not b_flag:
                for j in b_opps:

                    if j == game.team_b.tindex:
                        continue
                    item_set = self.remaining_opps(j, matchups, max_against)

                    if (b_opps.issubset(item_set) and item_set.issubset(b_opps)) or len(b_opps.intersection(item_set)) == 0:
                        b_flag = True


        if b_flag or a_flag: #if breaks try and
            return True
        else:
            return False

        # if either team now

    def remaining_opps(self, tindex, matchups, max_against):
        out = set()
        for i in range(len(matchups[0])):
            if matchups[tindex][i] < max_against:
                out.add(i)
        return out

    def get_games(self):
        return self.games.copy()

    def get_week(self):
        return self.week.copy()

    def get_matchups_state(self):
        #print(type(self.matchup_state))
        out = copy.deepcopy(self.matchup_state)
        return out
    def get_bye(self):
        return self.bye.copy()

    def set_bye(self, bye):
        self.bye = bye

    def get_trio_flag(self):
        return self.trio_flag

    def set_trio_flag(self, flag):
        self.trio_flag = flag
