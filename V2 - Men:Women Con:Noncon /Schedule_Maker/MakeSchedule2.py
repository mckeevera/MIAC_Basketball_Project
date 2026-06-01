# Required imports
import random
import numpy as np
import copy
import time

# Set seed(s)
random.seed(2332213)
np.random.default_rng(seed=42)


# Team names
teams = ["AUG", "BET", "CAR", "CON", "GAC", "HAM", "MAC", "SJU", "SMU", "STO", "CSS", "SCU"]

# Team numbers and name connections
team_numb = {
    "AUG": 0,
    "BET": 1,
    "CAR": 2,
    "CON": 3,
    "GAC": 4,
    "HAM": 5,
    "MAC": 6,
    "SJU": 7,
    "SMU": 8,
    "STO": 9,
    "CSS": 10,
    "SCU": 11,
}

# Repeated non-conference opponent restrictions
opp_requirements = {
    "AUG": {"fixed": ["CSS"],  # Always plays
            "p1": ["BET", "HAM", "SCU", "MAC"], "p1_r": (2, 3), # Plays 2 or 3 of
            "p2": ["SMU", "CON", "SJU", "CAR", "STO", "GAC"], "p2_r": (3, 4)}, # Plays 3 or 4 of
    "BET": {"fixed": ["CSS"], 
            "p1": ["AUG", "HAM", "SCU", "MAC"], "p1_r": (2, 3), 
            "p2": ["SMU", "CON", "SJU", "CAR", "STO", "GAC"], "p2_r": (3, 4)},
    "CAR": {"fixed": ["STO", "GAC", "SMU"], 
            "p1": [], "p1_r": (0, 0), 
            "p2": ["AUG", "BET", "HAM", "MAC", "SJU", "CON", "SCU", "CSS"], "p2_r": (4, 4)},
    "CON": {"fixed": ["SJU"], 
            "p1": ["CAR", "STO"], "p1_r": (2, 2), 
            "p2": ["GAC", "AUG", "BET", "HAM", "MAC", "SCU", "CSS"], "p2_r": (4, 4)},
    "GAC": {"fixed": ["STO", "CAR", "SMU"], "p1": [], "p1_r": (0, 0), 
            "p2": ["AUG", "BET", "HAM", "MAC", "SJU", "CON", "SCU"], "p2_r": (4, 4)},
    "HAM": {"fixed": ["CSS"], 
            "p1": ["BET", "AUG", "SCU", "MAC"], "p1_r": (2, 3), 
            "p2": ["SMU", "CON", "SJU", "CAR", "STO", "GAC"], "p2_r": (3, 4)},
    "MAC": {"fixed": ["CSS"], 
            "p1": ["BET", "HAM", "SCU", "AUG"], "p1_r": (2, 3), 
            "p2": ["SMU", "CON", "SJU", "CAR", "STO", "GAC"], "p2_r": (3, 4)},
    "SJU": {"fixed": ["CON"],
            "p1": ["AUG", "BET", "SCU", "HAM", "MAC"], "p1_r": (3, 4), 
            "p2": ["CAR", "STO", "GAC", "CSS"], "p2_r": (2, 3)},
    "SMU": {"fixed": ["STO", "GAC", "CAR"], 
            "p1": [], "p1_r": (0, 0), 
            "p2": ["AUG", "BET", "HAM", "MAC", "SCU"], "p2_r": (4, 4)},
    "STO": {"fixed": ["CAR", "GAC", "SMU"], 
            "p1": [], "p1_r": (0, 0), 
            "p2": ["AUG", "BET", "HAM", "MAC", "SJU", "CON", "SCU", "CSS"], "p2_r": (4, 4)},
    "CSS": {"fixed": ["AUG", "BET", "HAM", "SCU", "MAC"], 
            "p1": ["CAR", "STO", "SJU", "SMU", "CON"], "p1_r": (2, 2), 
            "p2": [], "p2_r": (0, 0)},
    "SCU": {"fixed": ["CSS"], 
            "p1": ["BET", "HAM", "MAC", "AUG"], "p1_r": (2, 3), 
            "p2": ["SMU", "CON", "SJU", "CAR", "STO", "GAC"], "p2_r": (3, 4)}
}

# Avoid bottle necks
steps = 0

# Check if a team can actually be a non-con opponent based on current schedyle
def is_valid(team, schedule):
    
    c = opp_requirements[team]
    
    opps = schedule[team]
    
    # If we have too many games for the team then it is not valid
    if len(opps) > 7: 
        return False
    
    # Get the number of opponents in the specific p1 or p2 subset
    p1_c = len([o for o in opps if o in c["p1"]])
    p2_c = len([o for o in opps if o in c["p2"]])
    
    # If we have too many in a specific subset then it is not valid
    if p1_c > c["p1_r"][1] or p2_c > c["p2_r"][1]: 
        return False
    
    # If we have 7 opponents but do not reach the minimum for each subset then it is not valid
    if len(opps) == 7:
        if p1_c < c["p1_r"][0] or p2_c < c["p2_r"][0]: 
            return False
        
    # If we pass all checks then it is valid
    return True


# Helper for generate_schedule
def solve(t_idx, current_teams, schedule):
    global steps
    steps += 1
    
    # Bottleneck avoidance
    if steps > 3000: 
        return False 

    # If we made it through all teams then we are done
    if t_idx == len(current_teams): 
        return True
    
    team = current_teams[t_idx]
    
    # If we completed the schedule for the team, move to the next
    if len(schedule[team]) == 7: 
        return solve(t_idx + 1, current_teams, schedule)

    # Get all possible opponents for the current team
    options = [o for o in (opp_requirements[team]["p1"] + opp_requirements[team]["p2"]) if o not in schedule[team]]
   
    # Randomally select the order in which we will test them
    random.shuffle(options)

    # For possible opponent
    for opp in options:
        
        # If we have space for another game
        if len(schedule[opp]) < 7:
            schedule[team].add(opp)
            schedule[opp].add(team)
            
            # Use is_valid to see if we can set this matchup and then use it, or backtrack and remove if we can't
            if is_valid(team, schedule) and is_valid(opp, schedule):
                if solve(t_idx, current_teams, schedule):
                    return True
            
            # Backtrack and remove
            schedule[team].remove(opp)
            schedule[opp].remove(team)
            
    return False

# Returns non-conference game schedule
def generate_schedule():
    global steps
    attempts = 0
    while True:
        attempts += 1
        steps = 0
        
        # Randomize order we schedule the teams
        shuffled_teams = list(teams)
        random.shuffle(shuffled_teams)
        
        # Add the games that we always use
        current_schedule = {t: set(opp_requirements[t]["fixed"]) for t in teams}
        
        # If we solved the schedule we move on, if not we loop
        if solve(0, shuffled_teams, current_schedule):
            return current_schedule


# Generate a schedule
final_schedule = generate_schedule()
retry_count = 1
max = 10000

# Schedule non-conference game opponents
# Loop for bottleneck protection
while retry_count < max:
    try:
        # Grab the selected opponents
        NonCon_Left = [list(final_schedule["AUG"]),
                        list(final_schedule["BET"]),
                        list(final_schedule["CAR"]),
                        list(final_schedule["CON"]),
                        list(final_schedule["GAC"]),
                        list(final_schedule["HAM"]),
                        list(final_schedule["MAC"]),
                        list(final_schedule["SJU"]),
                        list(final_schedule["SMU"]),
                        list(final_schedule["STO"]),
                        list(final_schedule["CSS"]),
                        list(final_schedule["SCU"])]

        NonCon_Sched = [[],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                []]

        # For each week
        for a in range(0,7):
            
            # Bottleneck avoidance
            time = 0
            
            # Make week 1
            for k in range(0,100):
                time = time + 1
                Can_Use = ["AUG", "BET", "CAR", "CON", "GAC", "HAM", "MAC", "SJU", "SMU", "STO", "CSS", "SCU"]

                home = []
                away = [] 
                
                # Set up 6 matchups
                for j in range(0, 6):  

                    # Pick a team 
                    pick = random.choice(Can_Use)
                        
                    home.append(pick)
                    Can_Use.remove(pick)

                    # Bottleneck avoidance
                    for i in range(0,1000):
                        
                        # Pick a possible opponent
                        away_pick = random.choice(NonCon_Left[team_numb[home[j]]])
                        
                        # Check if we can use and then do so if we can
                        if away_pick in Can_Use:
                            
                            away.append(away_pick)
                            Can_Use.remove(away_pick)
                            
                            break
                        
                        # else, try again
                        else:
                            pass
                # If we successfully got 6 matchups, move on        
                if len(away) == 6:
                    break
                
        
            # Tracking the schedyle
            for b in range(0,6):
                NonCon_Left[team_numb[home[b]]].remove(away[b])
                NonCon_Left[team_numb[away[b]]].remove(home[b])
                NonCon_Sched[team_numb[home[b]]].append(away[b])
                NonCon_Sched[team_numb[away[b]]].append(home[b])
                
        break        
        
    # If we get an error or fail, try again!
    except Exception:
        retry_count += 1
        #print(f"Retry {retry_count}/{max}...")
            
        if retry_count > 9998:
            print("This is rare! We failed to make a schedule 9999 times in a row! Please try again.") 

# List for non-con schedule
NonCon_Sched_number = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]

# Convert text names to numbers for the non-con schedule
for a in range(0,12):
    for b in range(0,7):
        NonCon_Sched_number[a][b] =  team_numb.get(NonCon_Sched[a][b])
        
        
# Loop to avoid bottlenecks
for a in range(0,10000):
    
    # Count number of home games for each team
    non_con_h_count = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    # Track location (2 as a placeholder)
    non_con_home_track = [[2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2]]

    # Now we home/away non-conference games
    # For each week
    for week in range (0,7):
        teams_to_ha = [0,1,2,3,4,5,6,7,8,9,10]

        # Loop through the 6 matches each week
        for i in range(0,6):
            # Pick a random team and see who they play that week
            pick = random.choice(teams_to_ha) 
            opp_str = NonCon_Sched[pick][week] 
            opp = team_numb[opp_str]

            # We will schedule team 11 last due to men/women team number disparity
            if opp == 11:
                teams_to_ha.remove(pick)
                
            # If the picked team has less home games than the opp, let them be home
            elif non_con_h_count[pick] < non_con_h_count[opp]:
                            non_con_home_track[pick][week] = 1 # 1 is home
                            non_con_home_track[opp][week] = -1 # -1 is away
                            teams_to_ha.remove(pick)
                            teams_to_ha.remove(opp)
                            non_con_h_count[pick] = non_con_h_count[pick] + 1
                            
            # If the picked team has more home games than the opp, let them be away
            elif non_con_h_count[opp] < non_con_h_count[pick]:
                            non_con_home_track[pick][week] = -1
                            non_con_home_track[opp][week] = 1
                            teams_to_ha.remove(pick)
                            teams_to_ha.remove(opp)
                            non_con_h_count[opp] = non_con_h_count[opp] + 1
                            
            # Otherwise, flip a coin
            else:
                            if random.randint(0, 1) == 0:
                                non_con_home_track[pick][week] = 1
                                non_con_home_track[opp][week] = -1     
                                teams_to_ha.remove(pick)
                                teams_to_ha.remove(opp)
                                non_con_h_count[pick] = non_con_h_count[pick] + 1

                            else:
                                non_con_home_track[pick][week] = -1
                                non_con_home_track[opp][week] = 1
                                teams_to_ha.remove(pick)
                                teams_to_ha.remove(opp)
                                non_con_h_count[opp] = non_con_h_count[opp] + 1
    
    # If we have 9 teams with 3 home games and 2 with 4 we continue
    if non_con_h_count.count(3) == 9 and  non_con_h_count.count(4) == 2:
        
        # Find the teams with 4 home games
        team4_1 = non_con_h_count.index(4)
        team4_2 = non_con_h_count.index(4, team4_1 + 1)

        # If they did not play SCU then we can continue
        if "SCU" not in NonCon_Sched[team4_1] and "SCU" not in NonCon_Sched[team4_2]:
            
            # SCU will play home against one of them
            SCU_Home = random.randint(3,4) 
            
            # See if each team plays SCU
            for team in range(0,11):
                try:
                    week_index = non_con_home_track[team].index(2)
                except ValueError:
                    week_index = None 
                    
                # If they play SCU then we set home away status in a similer manner to earlier
                if week_index != None:
                    if non_con_h_count[team] == 4:
                        non_con_home_track[team][week_index] = -1
                        non_con_home_track[11][week_index] = 1
                        non_con_h_count[11] = non_con_h_count[11] + 1

                    elif non_con_h_count[11] == SCU_Home:
                        non_con_home_track[team][week_index] = 1
                        non_con_home_track[11][week_index] = -1 
                        non_con_h_count[team] = non_con_h_count[team] + 1
                        
                    else:
                        if random.randint(0,1) == 0:
                            non_con_home_track[team][week_index] = -1
                            non_con_home_track[11][week_index] = 1
                            non_con_h_count[11] = non_con_h_count[11] + 1
                        else:
                            non_con_home_track[team][week_index] = 1
                            non_con_home_track[11][week_index] = -1 
                            non_con_h_count[team] = non_con_h_count[team] + 1
            
            # Now we should have a 6/6 split with SCU not scheduled
            if non_con_h_count.count(3) == 6 and  non_con_h_count.count(4) == 6:
                    passed = False
                    
                    no_11 = []
                    for z in range(0,11):
                        if "SCU" in NonCon_Sched[z]:
                            pass
                        else:
                            no_11.append(z)
                    
                    home_4 = []
                    home_3 = []
                    
                    # What teams have 4 games and which have 3 that do not play SCU (adding extra men's byes)
                    for item in no_11:
                        if non_con_h_count[item] == 4:
                            home_4.append(item)
                        else:
                            home_3.append(item)

                    # Randomize
                    random.shuffle(home_4)
                    random.shuffle(home_3)

                    # If we can remove these two games below and still have a 3/3 home/away split for every men's team then we continue
                    if home_3[0] in NonCon_Sched_number[home_4[0]]:
                        if home_3[1] in NonCon_Sched_number[home_4[1]]:
                            if non_con_home_track[home_4[0]][NonCon_Sched_number[home_4[0]].index(home_3[0])] == 1:
                                if non_con_home_track[home_4[1]][NonCon_Sched_number[home_4[1]].index(home_3[1])] == 1:
                                    extra_mens_bye1 = str(home_3[0]) + " @ " + str(home_4[0])
                                    extra_mens_bye2 = str(home_3[1]) + " @ " + str(home_4[1])    
                                    break
                                
                    # If we can remove these two games below and still have a 3/3 home/away split for every men's team then we continue
                    if home_3[0] in NonCon_Sched_number[home_4[1]]:
                        if home_3[1] in NonCon_Sched_number[home_4[0]]:
                            if non_con_home_track[home_4[1]][NonCon_Sched_number[home_4[1]].index(home_3[0])] == 1:
                                if non_con_home_track[home_4[0]][NonCon_Sched_number[home_4[0]].index(home_3[1])] == 1:
                                    extra_mens_bye1 = str(home_3[0]) + " @ " + str(home_4[1])
                                    extra_mens_bye2 = str(home_3[1]) + " @ " + str(home_4[0])
                                    break                

                
            if a > 9997:
                raise ValueError("Error - please try again")


# Next we turn our attention to conference games
# Restictions on when repeat games can be played to maintain large enough gaps before matchups repeat
non_con_restrictions = [[7,8,9,10],
                        [7,8,9,10],
                        [7,8,9,10],
                        [7,8,9,10],
                        [0,1],
                        [0,1,2],
                        [0,1,2]]

con_week_left = [[i for i in range(11)] for _ in range(12)]
con_schedule = [[-3 for _ in range(11)] for _ in range(12)]

# Order to schedule the weeks, (we do the more restricted ones first)
j_order = [4, 5, 6, 0, 1, 2, 3]

# Function to add all of the repeat matchups to the conference schedule
def solve_conference_schedule(j_list_index):

    # If we got through all weeks, move on
    if j_list_index >= len(j_order):
        return True

    # Get the non-con week games we are scheduling in the conference schedule
    j = j_order[j_list_index]
    
    # List of teams we are adding for this round
    teams_to_fix = []
    
    # Get teams and opponent for that round
    for i in range(12):
        opp = team_numb[NonCon_Sched[i][j]]
        
        if i < opp:
            teams_to_fix.append((i, opp))

    # Schedule the teams and opponents
    def schedule_pairs(pair_idx):
        
        # If we got rhough all of them, move to the next non-con week to add
        if pair_idx >= len(teams_to_fix):
            return solve_conference_schedule(j_list_index + 1)

        # The two teams
        team_a, team_b = teams_to_fix[pair_idx]
        
        # Grab which weeks we have left to use
        possible_weeks = non_con_restrictions[j][:]
        random.shuffle(possible_weeks)


        for week in possible_weeks:
           
            # See if we can schedule the game in this week
            if week in con_week_left[team_a] and week in con_week_left[team_b]:
                
                # Tracking
                con_week_left[team_a].remove(week)
                con_week_left[team_b].remove(week)
                con_schedule[team_a][week] = team_b
                con_schedule[team_b][week] = team_a
                
                # Continue to the next pair
                if schedule_pairs(pair_idx + 1):
                    return True
                
                # If we have no possible options, undo this selection and try again
                con_week_left[team_a].append(week)
                con_week_left[team_b].append(week)
                con_schedule[team_a][week] = -3
                con_schedule[team_b][week] = -3
        
        return False

    return schedule_pairs(0)

# If we did it and scheduled the games, move on
if solve_conference_schedule(0):
    pass
else:
    print("Error - please try again")
    
    
# remove already scheduled games (the repeat matchups)
con_left = [[item for item in [1,2,3,4,5,6,7,8,9,10,11]  if item not in con_schedule[0]],
            [item for item in [0,2,3,4,5,6,7,8,9,10,11]  if item not in con_schedule[1]],
            [item for item in [0,1,3,4,5,6,7,8,9,10,11]  if item not in con_schedule[2]],
            [item for item in [0,1,2,4,5,6,7,8,9,10,11]  if item not in con_schedule[3]],
            [item for item in [0,1,2,3,5,6,7,8,9,10,11]  if item not in con_schedule[4]],
            [item for item in [0,1,2,3,4,6,7,8,9,10,11]  if item not in con_schedule[5]],
            [item for item in [0,1,2,3,4,5,7,8,9,10,11]  if item not in con_schedule[6]],
            [item for item in [0,1,2,3,4,5,6,8,9,10,11]  if item not in con_schedule[7]],
            [item for item in [0,1,2,3,4,5,6,7,9,10,11]  if item not in con_schedule[8]],
            [item for item in [0,1,2,3,4,5,6,7,8,10,11]  if item not in con_schedule[9]],
            [item for item in [0,1,2,3,4,5,6,7,8,9,11]  if item not in con_schedule[10]],
            [item for item in [0,1,2,3,4,5,6,7,8,9,10]  if item not in con_schedule[11]]
                  ]


# Conference home track placeholders
con_home_track = [[2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2],
                        [2,2,2,2,2,2,2,2,2,2,2]]

# Change team numbers and names
numb_to_team = {v: k for k, v in team_numb.items()}

# Make the repeat conference games have the opposite home/away state as the non-conference ones
for a in range(0,12):
    for b in [0,1,2,7,8,9,10]:
        opp_number = con_schedule[a][b]
        team_string = numb_to_team[opp_number]
        con_home_track[a][b] = -1*non_con_home_track[a][NonCon_Sched[a].index(team_string)] # opposite of non-conference home/away status

# Teams
save_week_sked = [0,1,2,3,4,5,6,7,8,9,10,11]

# Backup copy of the current schedule in case we run into a bottleneck later
save_con_left = con_left
save_con_week_left = con_week_left
save_con_home_track = con_home_track
save_con_schedule = con_schedule

# Loop to avoid bottle neck
while True:
    try:    
        # We have four games to schedule, track how many home for each
        Con_FinalFour_HA_Track = [0,0,0,0,0,0,0,0,0,0,0,0]
        
        # Backup copies
        con_schedule = copy.deepcopy(save_con_schedule)
        con_home_track = copy.deepcopy(save_con_home_track)
        con_week_left = copy.deepcopy(save_con_week_left)
        con_left = copy.deepcopy(save_con_left)
        week_sked = copy.deepcopy(save_week_sked)
        
        success = True
        
        # for the games we have left to schedule
        for game_count in range(24):
            match_found = False
            
            # Figure out which teams have home games left
            eligible_home_teams = [t for t in range(12) if Con_FinalFour_HA_Track[t] < 2]
            
            # Break loop if out of home teams
            if not eligible_home_teams:
                break
                
            random.shuffle(eligible_home_teams)
            
            # Pick a home team
            for pick in eligible_home_teams:
                potential_opps = [o for o in con_left[pick]]
                random.shuffle(potential_opps)
                
                # Pick a random opponent
                for opp in potential_opps:
                    common_weeks = list(set(con_week_left[pick]) & set(con_week_left[opp]))
                    
                    # Check if we have a week in which they can play
                    if common_weeks:
                        week = random.choice(common_weeks)
                        
                        # Home/away them
                        con_home_track[pick][week] = 1
                        con_home_track[opp][week] = -1
                        Con_FinalFour_HA_Track[pick] += 1
                        
                        # Tracking
                        con_schedule[pick][week] = opp
                        con_schedule[opp][week] = pick
                        con_left[pick].remove(opp)
                        con_left[opp].remove(pick)
                        con_week_left[pick].remove(week)
                        con_week_left[opp].remove(week)
                        
                        
                        match_found = True
                        break
                    
                if match_found: 
                    break
            
            if not match_found:
                success = False
                break
            
        # If we scheduled all of the games and ended with 2 home and 2 away for each we move on
        if success and Con_FinalFour_HA_Track.count(2) == 12:
            break
            
    except:
        continue



# Print statements
print("Non Con Opponents")
print(NonCon_Sched_number)
print(non_con_home_track)

print("Con Opponents")
print(con_schedule)
print(con_home_track)

print("Extra Byes")
print(extra_mens_bye1)
print(extra_mens_bye2)


W_Schedule = [[],[],[],[],[],[],[],[],[],[],[],[]]

# Combine non-con and con games into schedule
for p in range (0,12):
        W_Schedule[p] = [NonCon_Sched_number[p][0], con_schedule[p][0], 
                         NonCon_Sched_number[p][1], con_schedule[p][1], 
                         NonCon_Sched_number[p][2], con_schedule[p][2],
                         NonCon_Sched_number[p][3], con_schedule[p][3],
                         con_schedule[p][4], con_schedule[p][5],
                         NonCon_Sched_number[p][4], con_schedule[p][6],
                         NonCon_Sched_number[p][5], con_schedule[p][7],
                         con_schedule[p][8], con_schedule[p][9],
                         NonCon_Sched_number[p][6], con_schedule[p][10],
                         
                         non_con_home_track[p][0], con_home_track[p][0], 
                         non_con_home_track[p][1], con_home_track[p][1], 
                         non_con_home_track[p][2], con_home_track[p][2],
                         non_con_home_track[p][3], con_home_track[p][3],
                         con_home_track[p][4], con_home_track[p][5],
                         non_con_home_track[p][4], con_home_track[p][6],
                         non_con_home_track[p][5], con_home_track[p][7],
                         con_home_track[p][8], con_home_track[p][9],
                         non_con_home_track[p][6], con_home_track[p][10]
                         
                         ]
        
print(W_Schedule)
# Men's schedule is the subset of this where team 11 is a bye week and we add in the two extra byes of extra_mens_bye1, extra_mens_bye2
