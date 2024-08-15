# This Python file uses the following encoding: utf-8



import copy
import math
from Game import Game
from Team import Team
from Week import Week
import random
from Season import Season


class League:
    name = ""
    matchups = None
    teams = None
    teams_hold = None
    max_games = None
    max_against = None
    bye = None
    season = None
    time_slots = None
    start_date = None
    s_week = 0
    in_group = False

    def __init__(self, name):
        self.name = name
        self.matchups = list()
        self.teams = dict()
        self.teams_hold = dict()
        self.bye = dict()
        self.time_slots = dict()

    def gen_season(self, games):
        self.matchup_init()
        self.teams_hold = self.teams.copy()
        self.set_max(games)
        self.season = Season()
        while not self.confirm_gp(self.max_against, True):
            self.season.reset_season()
            for team in self.teams:
                self.teams[team].reset_team()
            self.matchup_init()
            self.teams_hold = self.teams.copy()
            self.set_max(games)
            self.season_loop(games)
        print(self.confirm_gp(self.max_against, True))
        print(self.confirm_gp(self.max_against, False))
        self.season.print_season()
        for i in range(len(self.matchups[0])):
            print(self.matchups[i])

    def season_loop(self, games):
        week = 1
        week = self.round_robin(week)

        while not self.confirm_gp(self.max_games, True):
            if week > (self.max_games+(len(self.teams)%2+1)):
                print("Ending program")
                return False
            self.gen_week(week, self.bye)
            week += 1


    """
    Will continually try to generate a valid week
    Calls week loop to create a possible week, then checks if the week if valid and won't cause problems
    """
    def gen_week(self, week_num, bye):
        week = self.week_loop(week_num, bye)
        i = 0
        matchups_copy = copy.deepcopy(self.matchups)
        week.confirm_week(matchups_copy, self.max_against, copy.deepcopy(self.teams_hold))

        while not week.confirm_flag:
            week = self.week_loop(week_num, bye)
            week.confirm_week(matchups_copy, self.max_against, copy.deepcopy(self.teams_hold))
            i += 1
            if i >= 10:
                print("\n~~~Infinite loop entered~~~\n")
                break
        if week.confirm_flag:
            self.matchups = week.get_matchups_state()
            self.clean_hold()
            self.bye = week.bye
            self.season.add_week(week)
        else:
            print("Failed")
            return

    """
    Attempts to build a week
    """
    def week_loop(self, week_num, bye):
        temp = self.teams_hold.copy()
        bye = bye.copy()
        bye_out = {}
        week = Week(week_num)
        week.clear_week()
        key_list = list(temp.keys())

        for x in bye:
            team = bye[x]
            if team in temp:
                temp.pop(str(team.tindex))
            else:
                continue
            k_list = self.play_all(team, key_list)
            if k_list:
                b = self.find_matchup(team, temp, k_list)
            else:
                b = self.find_matchup(team, temp, key_list)
            if type(b) is Team:
                temp.pop(str(b.tindex))
                temp.pop(str(team.tindex))
                week.add_game(self.matchup(team, b))
            else:
                bye.pop(team)
                print("bye failed")
                bye_out.update({str(team.tindex): team})

        while len(temp) > 1:

            rand = random.randrange(len(temp))
            r = key_list.pop(rand)
            a = temp.pop(r)
            b = self.find_matchup(a, temp, key_list)
            if type(b) is Team:
                temp.pop(str(b.tindex))
                key_list.remove(str(b.tindex))
                week.add_game(self.matchup(a, b))
            else:
                bye_out.update({str(a.tindex): a})
                week.set_bye(bye_out)

        return week

    def round_robin(self, week_num):
        temp = self.teams_hold.copy()

        list_a = list()
        list_b = list()
        for i in range(math.ceil(len(temp)/2)):
            a = temp.pop(random.choice(list(temp.keys())))
            print("a: ",a)
            list_a.append(a)
            if temp:
                b = temp.pop(random.choice(list(temp.keys())))

            else:
                b = "Dummy"
            list_b.append(b)
            print("b: ",b)
        list_a_str = list()
        list_b_str = list()
        for i in range(len(list_a)):
            list_a_str.append(self.rr_test(list_a[i]))
            list_b_str.append(self.rr_test(list_b[i]))

        print(list_a_str)
        print(list_b_str)
        #print("[",list_a[0].name,',',list_a[1].name,',',list_a[2].name,',',list_a[3].name,']')
        #print("[", list_b[0].name, ',', list_b[1].name, ',', list_b[2].name, ',', list_b[3].name, ']')
        #print(list_a)
        #print(list_b)
        while week_num < (len(self.teams))+(len(self.teams)%2):
            week = Week(week_num)
            length = len(list_a)
            for i in range(length):
                a = list_a[i]
                b = list_b[i]
                if type(a) is Team and type(b) is Team:
                    game = self.matchup(a, b)
                    a.played_against(b)
                    b.played_against(a)
                    self.matchups[a.tindex][b.tindex] += 1
                    self.matchups[b.tindex][a.tindex] += 1
                else:
                    continue
            a = list_a.pop()
            b = list_b.pop(0)
            list_a.insert(1, b)
            list_b.append(a)
            list_a_str = list()
            list_b_str = list()
            for i in range(len(list_a)):
                list_a_str.append(self.rr_test(list_a[i]))
                list_b_str.append(self.rr_test(list_b[i]))

            print(list_a_str)
            print(list_b_str)
            print("End of week ", week_num,'\n-------------------------\n')
            week_num += 1

        for i in range(len(self.matchups[0])):
            print(self.matchups[i])
        return week_num

    def rr_test(self, item):
        if type(item) is Team:
            return item.name
        else:
            return item



    """
    Finds a matchup for the team 'a'
    takes in the team_hold dictionary and the keylist from week loop
    if a matchup is found passes out a team, else passes out False
    """
    def find_matchup(self, a, teams, key_list):

        i = random.randint(0, len(key_list) - 1)
        j = i
        found = False


        while i > -(len(key_list)) + j:

            if self.matchups[a.tindex][int(key_list[i])] < self.max_against:
                if self.last_mutual(a, teams[key_list[i]]):
                    out = i
                    found = True
                else:
                    out = i
                    found = True
                    break


            i -= 1
        if found:
            b = teams[key_list[out]]
            return b
        else:
            return False
    """
    Creates the matchups list
    """
    def matchup_init(self):
        self.matchups = []
        for i in range(len(self.teams)):
            self.matchups.append([])
            for j in range(len(self.teams)):
                self.matchups[i].append(0)

    """
    When a game has been verified the matchup is documented
    """
    def matchup(self, a, b):
        game = Game(a, b)
        return game

    """
    Checks if a matchup is valid
    """
    def matchup_check(self, a, b):
        if self.matchups[a.tindex][b.tindex] == self.max_against:
            return False
        else:
            return True

    def create_hold(self):
        self.teams_hold = self.teams.copy()

    """
    After a week has been confirmed checks that all teams haven't reached the max amount of games
    """
    def clean_hold(self):

        for i in range(len(self.matchups[0])):
            if sum(self.matchups[i]) == self.max_games and str(i) in self.teams_hold:
                self.teams_hold.pop(str(i))

    def set_max(self, max):
        self.max_games = max
        self.max_against = math.ceil(max / (len(self.teams) - 1))

    """
    Adds a team to the league
    """
    def add_team(self, name):
        print("add_team called")
        if type(name) is str:
            print("name is a string")
            if self.teams:
                print("teams is true")
                for team in self.teams:
                    print(self.teams[team].name)
                    if self.teams[team].name == name:
                        print("match found")
                        print(self.teams[team].name, "is the same as",name)
                        return False
            print("Attempting to create team: ", name)
            ind = len(self.teams)
            team = Team(name, ind, self)
            self.teams.update({str(ind): team})
            return True
        elif type(name) is Team:
            print("name is a team")
            name.set_tindex(len(self.teams))
            self.teams.update({str(name.tindex): name})
            name.set_league(self)
            return True



    """
    Checks if all teams have reached the desired amount of games
    alt parameter will change how the function works, accepts boolean or 1 to activate alt
    Returns flag(boolean)
    """
    def confirm_gp(self, max, alt):
        if alt or alt == 1:
            flag = True
            for i in range(len(self.matchups)):
                if sum(self.matchups[i]) != self.max_games:
                    flag = False
            return flag
        else:
            flag = True
            for t in self.teams:
                print(self.teams[t].name, "played ", self.teams[t].games_played, "games")
                if self.teams[t].games_played < max:
                    flag = False
            return flag

    """
    Takes in two teams and checks if they both played each other in their last game.
    Returns boolean
    """
    def last_mutual(self, a, b):
        if a.last == b.last and b.last == a.last and not (a.last is None or b.last is None):
            return True
        else:
            return False

    def play_all(self, a, key_list):
        k_list = set()
        key_list = set(key_list)
        count = self.matchups[a.tindex].count(0)
        if count == 1:
            return False
        ind = 0
        for i in range(0,count):
            ind = self.matchups[a.tindex].index(0,ind)
            if ind == a.tindex:
                continue
            k_list.add(str(ind))
        return list(k_list.intersection(key_list))

    def set_time_slots(self, time_slots):
        self.time_slots = copy.deepcopy(time_slots)
        print("setting time slots")
        print(self.time_slots)

    def set_start_date(self, date):
        self.start_date = date

    def share_time(self, league):
        for key in self.time_slots:
            if key in league.time_slots and len(self.time_slots[key] & league.time_slots[key]) > 0:
                return True
        return False 

    def get_av_games(self, day, time):
        out = set()
        for game in self.season.get_week(self.s_week).games:
            if day in game.avail_times:
                if time in game.avail_times[day]:
                    out.add(game)

                