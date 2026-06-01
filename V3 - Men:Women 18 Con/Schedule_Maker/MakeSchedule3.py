# Required imports
import random
import copy
from itertools import groupby
import csv

# Starting seed
curr_seed = 1

# Function to check the max home, away streak using groupby
def get_max(lst):
    m1 = max([len(list(g)) for k, g in groupby(lst) if k == 1] or [0])
    mn1 = max([len(list(g)) for k, g in groupby(lst) if k == -1] or [0])
    return (m1, mn1)

# Distance matrix recording travel time between locations
dist_mat = [
    # AUG BET CAR CON GAC HAM MAC SJU SMU STO CSS SCU
    [0,	18,	50,	212, 72, 12, 13, 77, 126, 47, 142,13],  # Row 0 AUG
    [18	,	0	,	59	,	209	,	82	,	16	,	20	,	74	,	131	,	56	,	134, 20],  # Row 1 BET
    [50	,	59	,	0	,	251	,	61	,	53	,	50	,	116	,	102	,	7	,	179, 50],  # Row 2 CAR
    [212	,	209	,	251	,	0	,	258	,	217	,	218	,	142	,	330	,	248	,	255, 218],  # Row 3 CON
    [72	,	82	,	61	,	258	,	0	,	79	,	77	,	123	,	137	,	59	,	206, 77],  # Row 4 GAC
    [12	,	16	,	53	,	217	,	79	,	0	,	11	,	82	,	124	,	49	,	141, 11],  # Row 5 HAM
    [13	,	20	,	50	,	218	,	77	,	11	,	0	,	84	,	125	,	47	,	143, 7],  # Row 6 MAC
    [77	,	74	,	116	,	142	,	123	,	82	,	84	,	0	,	195	,	113	,	167, 84],  # Row 7 SJU
    [126	,	131	,	102	,	330	,	137	,	124	,	125	,	195	,	0	,	105	,	229, 125],  # Row 8 SMU
    [47	,	56	,	7	,	248	,	59	,	49	,	47	,	113	,	105	,	0	,	177, 47],  # Row 9 STO
    [142	,	134	,	179	,	255	,	206	,	141	,	143	,	167	,	229	,	177	,	0, 143] , # Row 10 CSS
    [13	,	20	,	50	,	218	,	77	,	11	,	0	,	84	,	125	,	47	,	143, 0]# Row 11 SCU
]

# Avoiding bottleneck with loop
while True:
    
    try:
        # Set seed        
        random.seed(curr_seed)
        teams = ["AUG", "BET", "CAR", "CON", "GAC", "HAM", "MAC", "SJU", "SMU", "STO", "CSS", "SCU"]

        # Required men's repeat opponents
        M_Repeat_Opps_Raw = [
            [3,4,7,8,10,11,2,9], [3,4,7,8,10,11,2,9], [3,4,8,9,10,11,0,1,5,6],
            [0,1,2,5,6,7,9,10,11], [0,1,2,5,6,7,8,9,11], [3,4,7,8,10,11,2,9],
            [3,4,7,8,10,11,2,9], [0,1,3,4,5,6,8,10,11], [0,1,2,4,5,6,7,9,11],
            [2,3,4,8,10,11,0,1,5,6], [0,1,2,3,5,6,7,9,11], [0,1,2,3,4,5,6,7,8,9,10]
        ]

        # Function to add the additional men's opponents with a degree of randomness
        def apply_constraints(opps):
            
            # Backup copy
            constraints = copy.deepcopy(opps)
            
            # Pick which city team Carleton does not play, Olaf must play them
            CarCityOff = random.choice([0, 1, 5, 6])
            Sto_list = [0, 1, 5, 6]
            Sto_list.remove(CarCityOff)
            StOladCityOff = random.choice(Sto_list)

            # Tracking (Carleton plays their city teams, Olaf plays the other city teams, etc.)
            constraints[2].remove(CarCityOff)
            constraints[9].remove(StOladCityOff)
            constraints[StOladCityOff].remove(9)
            constraints[CarCityOff].remove(2)
            constraints[CarCityOff].append(StOladCityOff)
            constraints[StOladCityOff].append(CarCityOff)
            
            Sto_list.remove(StOladCityOff)
            city_1 = random.choice(Sto_list)
            Sto_list.remove(city_1)
            city_2 = Sto_list[0]

            constraints[StOladCityOff].append(city_1)
            constraints[CarCityOff].append(city_2)
            constraints[city_1].append(StOladCityOff)
            constraints[city_2].append(CarCityOff)
            return [sorted(list(set(row))) for row in constraints]

        # Get women's subset of repeat games using graph logic
        def get_7_regular_subset(constraints):
            
            # Set up the graph
            adj = [set(row) for row in constraints]
            
            for i in range(12):
                for neighbor in list(adj[i]): adj[neighbor].add(i)

            # Helper function that prunes the graph
            def solve(current_adj):
                degrees = [len(row) for row in current_adj]
                
                # Find teams that have more than 7 games
                if all(d == 7 for d in degrees): 
                    return current_adj
                idx = next(i for i, d in enumerate(degrees) if d > 7)
                
                # Find opponents that also have more than 7 games
                neighbors = [n for n in current_adj[idx] if len(current_adj[n]) > 7]
                
                # Randomize
                random.shuffle(neighbors)
                
                # Remove the extra game and repeat until we get a subset
                for neighbor in neighbors:
                    current_adj[idx].remove(neighbor)
                    current_adj[neighbor].remove(idx)
                    
                    result = solve(current_adj)
                    
                    if result is not None: 
                        return result
                    
                    current_adj[idx].add(neighbor)
                    current_adj[neighbor].add(idx)
                    
                return None

            res = solve(adj)
            return [sorted(list(row)) for row in res]



       # Function to randomize home and away locations for the teams
        def assign_home_away_randomized(adj_list):
            num_teams = len(adj_list)
            locales = [{} for _ in range(num_teams)]

            # Check that a team does not have more than 4 home or away games 
            def is_valid(team_idx):

                homes = sum(1 for opp, loc in locales[team_idx].items() if loc == 1 and opp != 11) # Count number of non-team 11 home games
                aways = sum(1 for opp, loc in locales[team_idx].items() if loc == -1 and opp != 11) # Count number of non-team 11 away games
                
                return homes <= 4 and aways <= 4 # True if valid, false otherwise

            # Bottleneck prevention function
            def backtrack(team_idx, opp_idx):
                if team_idx == num_teams: 
                    return True
                
                # If we have too many then backtrack
                if opp_idx >= len(adj_list[team_idx]): 
                    return backtrack(team_idx + 1, 0)
                
                opp = adj_list[team_idx][opp_idx]
                
                # If team 11 or already scheduled, backtrack
                if opp == 11 or team_idx == 11 or opp in locales[team_idx]:
                    return backtrack(team_idx, opp_idx + 1)

                # Home or away
                choices = [1, -1] 
                
                random.shuffle(choices)
                
            
                for choice in choices:
                    # Set home and away for the matchup
                    locales[team_idx][opp], locales[opp][team_idx] = choice, -choice
                    
                    # If we have a valid match up (for every team) move on
                    if is_valid(team_idx) and is_valid(opp):
                        if backtrack(team_idx, opp_idx + 1): 
                            return True
                        
                    del locales[team_idx][opp], locales[opp][team_idx]
                return False

            if backtrack(0, 0):
                return [[locales[i].get(opp, -2) for opp in adj_list[i]] for i in range(num_teams)]
            return None

        # Add team 11 locations (doing this last ensures that when 11 is a bye for Men we still have even H/A split)
        def finalize_with_team_11(adj_list, locales_list):
            
            # Backup copy
            locs = copy.deepcopy(locales_list)
            
            # SCU's home and away count
            t11_homes, t11_aways = 0, 0
            other_teams = list(range(11))
            random.shuffle(other_teams)
            
            # Decide locale for SCU
            for opp in other_teams:
                if 11 in adj_list[opp]:
                    idx_11 = adj_list[opp].index(11)
                    if t11_homes <= t11_aways:
                        locs[opp][idx_11] = -1 
                        t11_homes += 1
                    else:
                        locs[opp][idx_11] = 1 
                        t11_aways += 1
                        
            t11_row = []
            
            # Add the right location to SCU's schedule
            for opp_idx in adj_list[11]:
                idx_in_opp = adj_list[opp_idx].index(11)
                t11_row.append(-locs[opp_idx][idx_in_opp])
            locs[11] = t11_row
            return locs

        # Take the schedule locations and assign the same to Women
        def align_women_locales(m_opps, m_locs, w_opps):
            w_locs = []
            for i in range(12):
                
                # Get men locations
                m_lookup = {opp: loc for opp, loc in zip(m_opps[i], m_locs[i])}
                
                # Add them to women locations
                w_locs.append([m_lookup[opp] for opp in w_opps[i]])
            return w_locs

        # Check that the women schedule is a 3/4 split or 4/3 split
        def is_women_balanced(w_locs):
            return all(3 <= row.count(1) <= 4 for row in w_locs)

        
        # Get repeat opponents        
        M_Rep_Opps = apply_constraints(M_Repeat_Opps_Raw)
        W_Rep_Opps = get_7_regular_subset(M_Rep_Opps)

        # Variable set up
        M_Rep_Locale, W_Rep_Locale = None, None
        
        # Attempt counter
        for attempt in range(200):
            # Assign hpme and away
            m_base = assign_home_away_randomized(M_Rep_Opps)
            if m_base:
                # SCU work
                m_final = finalize_with_team_11(M_Rep_Opps, m_base)
                # Check that Women's subset schedule works
                w_final = align_women_locales(M_Rep_Opps, m_final, W_Rep_Opps)
                if is_women_balanced(w_final):
                    M_Rep_Locale, W_Rep_Locale = m_final, w_final
                    break

        # Now we turn the focus to scheduling the games and the round robin we have left.
        final_success = False
        
        # Bottleneck avoidance loop
        for attempt_p1 in range(100): 
            
            # Set up lists
            DH_Home_Count = [0]*12
            M_Sched_Opps = [[-2]*18 for _ in range(12)]
            M_Sched_Loc = [[-2]*18 for _ in range(12)]
            M_Base_Pool = [list(range(12)) for _ in range(12)]
            for i in range(12): M_Base_Pool[i].remove(i)

            schedule_ruined = False
            
            # We save these weeks for the doubleheaders (Saturdays)
            base_weeks = [0,1,2,3,5,7,9,11,13,15,17]
            
            # for each DH week
            for a in base_weeks:
                week_success = False
                
                # Bottleneck avoifance loop
                for attempt in range(250):
                    
                    # Backup
                    Pool_Backup = copy.deepcopy(M_Base_Pool); H_Backup = copy.deepcopy(DH_Home_Count)
                    Available = list(range(12))
                    for _ in range(1000):
                        
                        # If we got through all teams, move on
                        if not Available: 
                            week_success = True; break
                            
                        team = random.choice(Available)
                        
                        # Check possible opponents for the selected team
                        possible = [o for o in M_Base_Pool[team] if o in Available]
                        # Remove opponents that are within 4 rounds (no use case currently, but could be used if more games were played)
                        lookback = [M_Sched_Opps[team][w] for w in range(max(0, a-12), a)]
                        possible = [o for o in possible if o not in lookback]
                        # If we have no possible options, backtrack
                        if not possible: 
                            break
                        opp = random.choice(possible)
                        
                        forced_loc = 0 
                        # If this is a repeat game, force the opposite locations, otherwise use 99 as an open placeholder
                        if opp in M_Rep_Opps[team]:
                            side = M_Rep_Locale[team][M_Rep_Opps[team].index(opp)]
                        else:
                            side = 99
                        
                        # Tracking
                        M_Sched_Opps[team][a], M_Sched_Opps[opp][a] = opp, team
                        M_Sched_Loc[team][a], M_Sched_Loc[opp][a] = -side, side
                        if side == 1: 
                            DH_Home_Count[team] += 1
                        else: 
                            DH_Home_Count[opp] += 1
                        M_Base_Pool[team].remove(opp); M_Base_Pool[opp].remove(team)
                        Available.remove(team); Available.remove(opp)
                    # If we did it, move on
                    if week_success: 
                        break
                    # If we failed to make the week, try again
                    else: M_Base_Pool, DH_Home_Count = copy.deepcopy(Pool_Backup), copy.deepcopy(H_Backup)
                if not week_success: schedule_ruined = True; break
                
            # If we scheduled all of the weeks, check to see if we have a home game for each team in the last two DH weeks
            # If not, try again
            if not schedule_ruined: 
                if all(M_Sched_Loc[t][15] == 1 or M_Sched_Loc[t][17] == 1 for t in range(12)): 
                    
                    final_success = True; break


        # Back up schedules
        W_Sched_Loc = copy.deepcopy(M_Sched_Loc)

        W_Sched_Opps = copy.deepcopy(M_Sched_Opps)

       # Now we schedule the repeat games in the remaining weeks  
        def fill_repeats_final(Sched_Opps, Sched_Locale, repeat_pool, repeat_locale):
                for attempt_phase in range(10): 
                    # Backup schedules
                    sched_opps = copy.deepcopy(Sched_Opps)
                    sched_loc = copy.deepcopy(Sched_Locale)
                    rem_repeats = copy.deepcopy(repeat_pool)
                    failed_phase = False
                    
                    # For remaining week
                    for a in [4, 6, 8, 10, 12, 14, 16]:
                        week_success = False
                        
                        # Bottle neck avoidance
                        for attempt in range(500):
                            rep_backup = copy.deepcopy(rem_repeats); avail = list(range(12))
                            for _ in range(1000):
                                if not avail: 
                                    week_success = True; break
                                t = random.choice(avail)
                                
                                # Pick a team's possible opponents
                                possible = [o for o in rem_repeats[t] if o in avail]
                                
                                # Remove opponents that were played in the round robin games in adjacent weeks (avoid back to back matchups)
                                lookback = [sched_opps[t][prev] for prev in range(max(0, a-2), a)]
                                lookahead = [sched_opps[t][fwd] for fwd in range(a+1, min(18, a+5))]
                                possible = [o for o in possible if o not in lookback and o not in lookahead]
                                
                                # If no possible opponents, break and try again
                                if not possible: 
                                    break
                                
                                # Otherwise, we pick an opponent and track
                                o = random.choice(possible)
                                sched_opps[t][a], sched_opps[o][a] = o, t
                                rem_repeats[t].remove(o); rem_repeats[o].remove(t)
                                avail.remove(t); avail.remove(o)
                                
                                
                                sched_loc[t][a], sched_loc[o][a] = repeat_locale[t][repeat_pool[t].index(o)], -repeat_locale[t][repeat_pool[t].index(o)]                      
                # If we get through all teams and all weeks move on, otherwise try again                   
                            if week_success: break
                            else: rem_repeats = copy.deepcopy(rep_backup)
                        if not week_success: failed_phase = True; break
                    if not failed_phase: return sched_opps, sched_loc, rem_repeats
                return None, None, None 
            
        # Fill in repeat schedule for Men  
        M_O_Final, M_L_Final, M_Rem = fill_repeats_final(M_Sched_Opps, M_Sched_Loc, M_Rep_Opps, M_Rep_Locale)

        # Fill in repeat schedule for Women
        W_O_Final, W_L_Final, W_Rem = fill_repeats_final(W_Sched_Opps, W_Sched_Loc, W_Rep_Opps, W_Rep_Locale)

        # Now, Men have two extra games to fill in (because of bye weeks)
        def fill_weeks_18_19_consistent(m_rem, current_sched_opps, current_sched_loc, m_opps, m_locs):
            
            # Backup lists
            final_opps = copy.deepcopy(current_sched_opps)
            final_loc = copy.deepcopy(current_sched_loc)
            rem_repeats = copy.deepcopy(m_rem)

            # Add two extra weeks to the Men schedules
            for i in range(12):
                while len(final_opps[i]) < 20:
                    final_opps[i].append(-2)
                    final_loc[i].append(-2)

            # For each week
            for week in [18, 19]:
                available = list(range(12)) # Include all 12 teams
                random.shuffle(available)
                
                # Add extra bye weeks to ensure each team gets two byes
                available.append(11)
                available.append(11)
                available.append(11)

                while available:
                    # Pick a team
                    t = available.pop(0)
                    
                    # Get an opponent
                    possible = [o for o in rem_repeats[t] if o in available]
                    
                    if possible:
                        opp = possible[0]
                        available.remove(opp) 
                        
                        # Schedule the opponent
                        final_opps[t][week], final_opps[opp][week] = opp, t
                        
                        # Assign the game location based on the repeat matchup from earlier
                        idx_for_t = m_opps[t].index(opp)
                        side = m_locs[t][idx_for_t]
                        
                        final_loc[t][week], final_loc[opp][week] = side, -side
                        
                        # Tracking
                        rem_repeats[t].remove(opp)
                        rem_repeats[opp].remove(t)
                    else:
                        # If no opponents schedule as a -2 placeholder
                        final_opps[t][week] = -2
                        final_loc[t][week] = -2

            return final_opps, final_loc

        # Add the extra two weeks
        M_O_Final, M_L_Final = fill_weeks_18_19_consistent(M_Rem, M_O_Final, M_L_Final, M_Rep_Opps, M_Rep_Locale)
        
        # Bottleneck protection for adding the extra two weeks
        alpha = 0
        # Check if we can actually assign the two extra games in two weeks, that is we did not have to use -2 earlier in fill_weeks_18_19_consistent
        while True:
            Output_1, Output_2 = fill_weeks_18_19_consistent(M_Rem, M_O_Final, M_L_Final, M_Rep_Opps, M_Rep_Locale)
            is_present = any(-2 in sublist for sublist in Output_1[:-1])
            alpha += 1
            if alpha > 10:
                raise ValueError()
            if not is_present:
                M_O_Final, M_L_Final =Output_1, Output_2
                break

        # Now we assign the non-repeated opponents locations that we assigned as 99 (or -99)
        def fix_placeholders_and_balance(sched_opps, sched_loc):
            
            # Backup
            fixed_loc = copy.deepcopy(sched_loc)
            num_teams = len(sched_opps)
            num_weeks = len(sched_opps[0])
            
            # Bottleneck protection
            for _ in range(50): 
                # For each team, for each week
                for i in range(num_teams):
                    for week in range(num_weeks):
                        opp = sched_opps[i][week]
                        
                        # If already scheduled then don't do anything
                        if fixed_loc[i][week] in [99, -99, -2]:
                            # If a bye then skip
                            if opp == -2: 
                                continue
                                
                            # Count home - away games (a bit cleaner than counting both like we did earlier)
                            i_balance = fixed_loc[i].count(1) - fixed_loc[i].count(-1)
                            opp_balance = fixed_loc[opp].count(1) - fixed_loc[opp].count(-1)
                            
                            # Assign home to the team that has less home games
                            if i_balance < opp_balance:
                                fixed_loc[i][week] = 1
                                fixed_loc[opp][week] = -1
                            elif opp_balance < i_balance:
                                fixed_loc[i][week] = -1
                                fixed_loc[opp][week] = 1
                            else:
                                # Otherwise flip a coin if they are tied
                                side = random.choice([1, -1])
                                fixed_loc[i][week] = side
                                fixed_loc[opp][week] = -side
                                
            return fixed_loc


        # Assign the last few home/away locations
        M_L_Final = fix_placeholders_and_balance(M_O_Final, M_L_Final)
        W_L_Final = fix_placeholders_and_balance(W_O_Final, W_L_Final)

        # We check home counts for each team, exclude_SCU is True for Men which makes it act like a bye
        def get_home_count_list(sched_opps, sched_loc, exclude_scu=False):
            home_counts = []
            for i in range(12):
                h_count = 0
                
                # Count for each team
                for w in range(len(sched_opps[i])):
                    opp = sched_opps[i][w]
                    loc = sched_loc[i][w]
                    
                    # Men
                    if exclude_scu:
                        
                        if opp != 11 and opp != -2 and loc == 1:
                            h_count += 1
                            
                    # Women
                    else:
                        if opp != -2 and loc == 1:
                            h_count += 1
                home_counts.append(h_count)
            return home_counts
        


    # Catch all error that will try again with a new seed
    except Exception as e:
        curr_seed = curr_seed + 1
        print(f"Seed failed, trying: {curr_seed}")
        
    # Otherwise, we have a schedule and we can view it and save it!
    else:
        
        

        # Get home counts
        m_home_list = get_home_count_list(M_O_Final, M_L_Final, exclude_scu=True)
        m_home_list.pop() # Remove SCU since it is really just the bye
        w_home_list = get_home_count_list(W_O_Final, W_L_Final, exclude_scu=False)
        
        # Check that we have 9/9 home and away splits (i.e. the only value is 9)
        is_single_value_M= len(set(m_home_list)) == 1
        is_single_value_W = len(set(w_home_list)) == 1

        # If we have the right counts continue
        if is_single_value_M and is_single_value_W:
            
            # Check when the Saturday double headers do not line up (we will still (almost) always have 9 or more even when there are some mismatches)
            # These occur when trying to balance the 9/9 split
            def count_even_week_mismatches(m_loc, w_loc, teams):
                
                # Nice header
                print(f"\n--- HOME/AWAY MISMATCHES (EVEN WEEKS) ---")
                print(f"{'TEAM':<6} | {'MISMATCHES':<10} | {'WEEKS'}")
                print("-" * 40)
                
                total_mismatches = 0
                num_weeks = len(m_loc[0])
                
                # For each team
                for i in range(12):  
                    team_mismatches = 0
                    mismatch_weeks = []
                    
                    # Track if the locations are different on Saturdays
                    for w in [1,3,5,7,9,11,13,15,17]:
                        m_side = m_loc[i][w]
                        w_side = w_loc[i][w]
                        
                        # If they are not on bye (really only applies to Men)
                        if m_side != -2 and w_side != -2:
                            
                            # If the location does not match we have a mismatch
                            if m_side != w_side:
                                team_mismatches += 1
                                mismatch_weeks.append(w + 1)
                    
                    total_mismatches += team_mismatches
                    
                    # Show the number of mismatches (or none if there are 0) for each team
                    weeks_str = ", ".join(map(str, mismatch_weeks)) if mismatch_weeks else "None"
                    print(f"{teams[i]:<6} | {team_mismatches:<10} | {weeks_str}")

                print("-" * 40)
                print(f"Total Saturday Mismatches: {total_mismatches}")

            # Check the mismatches on Saturdays
            count_even_week_mismatches(M_L_Final, W_L_Final, teams)
            
            # Calculate distance for each team using the distance matrix
            M_Dist = [0,0,0,0,0,0,0,0,0,0,0]
            for j in range(0,11):
                for i in range(0,20):
                    # If on bye skip
                    if M_O_Final[j][i] == 11:
                        pass
                    elif M_L_Final[j][i] == -1:
                        M_Dist[j] = M_Dist[j] + dist_mat[j][M_O_Final[j][i]]
                    else:
                        pass
            
            W_Dist = [0,0,0,0,0,0,0,0,0,0,0,0]
            for j in range(0,12):
                for i in range(0,18):
                    if W_L_Final[j][i] == -1:
                        W_Dist[j] = W_Dist[j] + dist_mat[j][W_O_Final[j][i]]
                    else:
                        pass
            #print(M_Dist)
            #print(W_Dist)

            # Calculate the gaps between byes for men
            bye_gaps = []
            for sublist in M_O_Final[:-1]:
                # We ignore the last two weeks since they are bonus weeks to fit in the 18 games
                truncated_list = sublist[:-2]
                
                # Where are byes played
                indices = [i for i, val in enumerate(truncated_list) if val == 11]
                
                # Calculate the bye gap
                if len(indices) >= 2:
                    gap = indices[1] - indices[0] - 1
                    bye_gaps.append(gap)
                else:
                    bye_gaps.append(0)

            print(f"Bye Gaps: {bye_gaps}")
            
            # Get the max home and away streak for each team
            M_Streak = [get_max(sub) for sub in M_L_Final]            
            W_Streak = [get_max(sub) for sub in W_L_Final]

            M_Streak.pop() # Remove SCU since it is really just the bye
            #print(M_Streak)
            #print(W_Streak)
            
            # CSV
            Full_CSV = [[],[],[],[],[],[],[],[],[],[],[],
                        [],[],[],[],[],[],[],[],[],[],[],[]]
            
            # Add all of our schedule information
            for i in range(0,11):
                Full_CSV[i] = [curr_seed, "M", M_Dist[i], bye_gaps[i], M_Streak[i][0], M_Streak[i][1], 
                               M_O_Final[i][0], M_O_Final[i][1], M_O_Final[i][2], M_O_Final[i][3], M_O_Final[i][4], 
                               M_O_Final[i][5], M_O_Final[i][6], M_O_Final[i][7], M_O_Final[i][8], M_O_Final[i][9], 
                               M_O_Final[i][10], M_O_Final[i][11], M_O_Final[i][12], M_O_Final[i][13], M_O_Final[i][14], 
                               M_O_Final[i][15], M_O_Final[i][16], M_O_Final[i][17], M_O_Final[i][18], M_O_Final[i][19], 
                               M_L_Final[i][0], M_L_Final[i][1], M_L_Final[i][2], M_L_Final[i][3], M_L_Final[i][4], 
                               M_L_Final[i][5], M_L_Final[i][6], M_L_Final[i][7], M_L_Final[i][8], M_L_Final[i][9], 
                               M_L_Final[i][10], M_L_Final[i][11], M_L_Final[i][12], M_L_Final[i][13], M_L_Final[i][14], 
                               M_L_Final[i][15], M_L_Final[i][16], M_L_Final[i][17], M_L_Final[i][18], M_L_Final[i][19] 
                               ]
                
            for j in range(0,12):
                Full_CSV[j+11] = [curr_seed, "W", W_Dist[j],  "NA", W_Streak[j][0], W_Streak[j][1], 
                               W_O_Final[j][0], W_O_Final[j][1], W_O_Final[j][2], W_O_Final[j][3], W_O_Final[j][4], 
                               W_O_Final[j][5], W_O_Final[j][6], W_O_Final[j][7], W_O_Final[j][8], W_O_Final[j][9], 
                               W_O_Final[j][10], W_O_Final[j][11], W_O_Final[j][12], W_O_Final[j][13], W_O_Final[j][14], 
                               W_O_Final[j][15], W_O_Final[j][16], W_O_Final[j][17], "NA",  "NA", 
                               W_L_Final[j][0], W_L_Final[j][1], W_L_Final[j][2], W_L_Final[j][3], W_L_Final[j][4], 
                               W_L_Final[j][5], W_L_Final[j][6], W_L_Final[j][7], W_L_Final[j][8], W_L_Final[j][9], 
                               W_L_Final[j][10], W_L_Final[j][11], W_L_Final[j][12], W_L_Final[j][13], W_L_Final[j][14], 
                               W_L_Final[j][15], W_L_Final[j][16], W_L_Final[j][17],  "NA",  "NA"
                ]
            
            # Print the CSV to the user and output as CSV
            print(Full_CSV)
            with open('Out.csv', 'a') as f:
                writer = csv.writer(f)
                for item in Full_CSV:
                    writer.writerow(item) 
            
        # If we failed at the final steps (or made a schedule correctly) move on to the next seed to try again 
        curr_seed = curr_seed + 1
        print(f"Seed failed, trying: {curr_seed}")