# This Python file uses the following encoding: utf-8

"""
How Time slot/block data is currently stored:

    From their first instantiation by the gen_ functions in mainwindow time data is stored in Dictionaries, where the keys
    are the strings used in the headers of the TableWidgets.  Similar to week_dict below, except in the case of week_dict 
    hours are also a dictionary containing a set.  My original thought fill all sets each week with whatever games were available. 

How it's supposed to work:

1. Split the leagues into groups. (LeagueGroup.py)

        A league is added to the group if it shares a League.time_slots day with any other league.  
        This is why the create_group function is called twice.

2. Go through each group and assign schedules that way.

        Leagues have different start dates, possibly even within groups.  Due to this each League object has 
        an attribute called s_week or "season week".  Matchups are generated prior to assigning them to dates by the league
        class.  Matchups are separated into Week objects, which contain Game objects.  These week objects are all contained 
        leagues season attribute.  

        Both League and Game have methods for verifying time slots.  When a game is created it will check the time slots of 
        the leagues of both teams, against the time blocks of both teams, and create a dictionary.  League has the function 
        get_av_games(day, time) which takes the weekday and the hour and will return a set of all games in League.games[s_week] 
        that can be scheduled for that hour.

        Hours in the middle are to be prioritized for scheduling; 6, 9, and 10 are to be avoided if possible
    
    3. First check if any games only have one available time_slot.  Assign them first

    4. Next assign games to middle time slots.  Before confirming a placement, check that the placement wouldn't leave any other 
       games with no available slots.  Continue until finished 

            Current thought is check the set.difference(all free time_slots) as well as 
            set.intersection(all free slots and remaining games in current av_games).  If the difference contains any of the
            av_games, assign it.  If the intersection does not contain all remaining av games, take the difference now including
            remaining av_games and assign the difference to the current time slot instead.
    
    5. If the week is successful, iterate s_week in each league in the group that had games assigned this week.  
"""

from LeagueGroup import LeagueGroup
import copy
class Schedule:

    league_coll = None
    week_dict = {"Sun": {"6:00": set(), "7:00": set(), "8:00": set(), "9:00": set(), "10:00": set()}, 
                 "Mon": {"6:30": set(), "7:30": set(), "8:30": set(), "9:30": set()}, 
                 "Tues": {"6:00": set(), "7:00": set(), "8:00": set(), "9:00": set(), "10:00": set()}, 
                 "Wed": {"6:00": set(), "7:00": set(), "8:00": set(), "9:00": set(), "10:00": set()}, 
                 "Thurs": {"6:00": set(), "7:00": set(), "8:00": set(), "9:00": set(), "10:00": set()}, 
                 "Fri": {"6:30": set(), "7:30": set(), "8:30": set(), "9:30": set()},
                 "Sat": {"6:00": set(), "7:00": set(), "8:00": set(), "9:00": set(), "10:00": set()}}

    def __init__(self):
        pass

    #if leagues share time slots add them to a collection together
    def create_collections(self, leagues):
        league_coll = list()
        done = set()
        for day in self.week_dict:
            if day in done:
                 continue
            for key in leagues:
                if leagues[key].in_group:
                     continue
                if day in leagues[key].time_slots:
                    group = LeagueGroup(day, leagues[key])
                    self.create_group(leagues, group)
                    self.create_group(leagues, group) #calls the function twice to ensure every team that can be added is
                    league_coll.append(group)
                    done = done | group.week_days
                    group = None
                    break
        #for lgroup in league_coll:
             #for day in lgroup.week_days:
                  #lgroup.hold_add(day, copy.deepcopy(self.week_dict[day]))
        self.league_coll = league_coll
                        
    def create_group(self, leagues, group):
                for key in leagues:
                    if leagues[key] in group.leagues:
                        continue
                    group.add_league(leagues[key])
                    
            

    

    #for each time slot in collection, create a set of games that can be assigned
        #preferred times are in the middle, so 7 and 8 or 730 and 830, attempt to assign those games first
            #attempt to assign games to the time slot in ascending order by len(game.avail_times)
            #if intersection of all remaining games < number of remaining time slots: fail
