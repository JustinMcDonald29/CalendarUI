from League import League
from Weekday import Weekday

def test():


    league = League("Men's 1")
    league.add_team("One")
    league.add_team("Two")
    league.add_team("Three")
    league.add_team("Four")
    league.add_team("Five")
    league.add_team("Six")
    league.add_team("Seven")
    league.add_team("Eight")
    
    time_slots = {"Wed": {"6:00", "7:00", "8:00", "9:00", "10:00"},"Thurs": {"6:00", "7:00", "8:00", "9:00", "10:00"}}
    league.set_time_slots(time_slots)
    
    #print(Weekday.from_dict(time_slots))
    league.teams['2'].set_time_blocks({"Thurs": {"10:00"}}) #three
    league.teams['3'].set_time_blocks({"Thurs": {"8:00"}}) #four
    league.teams['5'].set_time_blocks({"Thurs": {"9:00"}}) #six
    league.teams['7'].set_time_blocks({"Thurs": {"6:00", "10:00"}}) #eight

    league2 = League("Men's 2")
    league2.add_team("Un")
    league2.add_team("Deux")
    league2.add_team("Trois")
    league2.add_team("Quatre")
    league2.add_team("Cinq")
    league2.add_team("Sixx")
    league2.add_team("Sept")
    league2.add_team("Huit")

    league2.set_time_slots(time_slots)

    league.teams['0'].set_time_blocks({"Wed": {"10:00"}}) #Un
    league.teams['2'].set_time_blocks({"Wed": {"8:00"}}) #Trois
    league.teams['4'].set_time_blocks({"Wed": {"9:00"}}) #Cinq
    league.teams['6'].set_time_blocks({"Wed": {"6:00", "10:00"}}) #Sept
    

    league.gen_season(10)
    gen_schedule(league)



def gen_schedule(league):
    season = league.get_season()
    final_schedule = list()
    
    def schedule_week(week, time_slots):      
        print("Scheduling week:")

        def backtrack(schedule, index):
            if index == len(week):  # All matchups are scheduled
                return schedule

            current_matchup = week[index]
            for time in time_slots:
                if time in Weekday.from_dict(current_matchup.get_av_times()) and time not in schedule.values():  # Check if time slot is valid
                    current_matchup.set_time(time)
                    schedule[current_matchup.code] = time  # Schedule the matchup
                    result = backtrack(schedule, index + 1)  # Recursively schedule the next matchup
                    if result:  # If valid schedule found, return it
                        return result
                    del schedule[current_matchup]  # Backtrack
                    current_matchup.set_time(None)

            return None  # No valid schedule found

        return backtrack(dict(), 0)  # Start with an empty schedule and the first matchup
    
    for i in range(len(season.season)):
        print("gen_schedule")
        week = season.get_games(i)
        time_slots = Weekday.from_dict(league.time_slots)
        week.sort(key=lambda m: m.con_len)
        final_schedule.append(schedule_week(week, time_slots))
    print(final_schedule)
test()
