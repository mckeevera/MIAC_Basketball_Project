# Required Imports
import random
import csv

# Schdule index (to group schedules)
schedule = 0

# Number of schedules to create
iter = 1

# Distance check function that returns the distance between two teams (and 0 if the team is on bye)
def distance(A, B):
    if (A == -1):
        return 0
    if (B== -1):
        return 0
    
    d = dist_matrix[A][B]
    return d

# Function that selects the non conference games to be played
def create_noncon():
    
    # for loop to avoid bottlenecks
    for j in range(1,100):   
        
        # Non Conference teams to play, we build this in these lists in the function, we start with some already implemented based on opponents that 'make sense' to always play
        NonCon_Left = [[10], # AUG - 0
               [10], # Bet - 1
               [9,4,8], # CAR - 2
               [7], # CON - 3
               [9,2,8], # GAC - 4
               [10], # HAM - 5
               [10], # MAC - 6
               [3], # SJU - 7
               [9,4,2], # SMU - 8
               [2,4,8], # STO - 9
               [0,1,5,6]] # CSS - 10
        
        # Track games that need to be selected, each team needs a total of 6 games
        NonCon_To_Schedule = [0,0,0,0,0,1,1,1,1,1,2,2,2,3,3,3,3,3,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,9,9,9,10,10]

        # Carleton/Olaf/Marys selection 
        # Pick random teams to play
        dummy = [2,7,9]
        choice1 = random.choice(dummy)
        dummy.remove(choice1)
        choice2 = random.choice(dummy)

        # Track teams that have to play each other
        NonCon_Left[10].append(choice1)
        NonCon_Left[10].append(choice2)
        NonCon_Left[choice1].append(10)
        NonCon_Left[choice2].append(10)

        NonCon_To_Schedule.remove(choice1)
        NonCon_To_Schedule.remove(choice2)
        NonCon_To_Schedule.remove(10)
        NonCon_To_Schedule.remove(10)

        # City teams selections
        dummy = [1,5,6]
        choice1 = random.choice(dummy)
        dummy.remove(choice1)
        choice2 = random.choice(dummy)
        dummy.remove(choice2)
        
        # Track teams that have to play each other
        NonCon_Left[0].append(choice1)
        NonCon_Left[0].append(choice2)
        NonCon_Left[choice1].append(0)
        NonCon_Left[choice2].append(0)
        NonCon_To_Schedule.remove(0)
        NonCon_To_Schedule.remove(0)
        NonCon_To_Schedule.remove(choice1)
        NonCon_To_Schedule.remove(choice2)

        not_play = dummy[0]

        NonCon_Left[not_play].append(choice1)
        NonCon_Left[not_play].append(choice2)
        NonCon_Left[choice1].append(not_play)
        NonCon_Left[choice2].append(not_play)

        NonCon_To_Schedule.remove(not_play)
        NonCon_To_Schedule.remove(not_play)
        NonCon_To_Schedule.remove(choice1)
        NonCon_To_Schedule.remove(choice2)

        # Find city teams the Mary's plays 
        dummy = [0,1,5,6]
        choice1 = random.choice(dummy)
        dummy.remove(choice1)
        choice2 = random.choice(dummy)
        dummy.remove(choice2)
        choice3 = random.choice(dummy)
        
        # Track teams that have to play each other
        NonCon_Left[8].append(choice1)
        NonCon_Left[8].append(choice2)
        NonCon_Left[8].append(choice3)

        NonCon_Left[choice1].append(8)
        NonCon_Left[choice2].append(8)
        NonCon_Left[choice3].append(8)

        NonCon_To_Schedule.remove(8)
        NonCon_To_Schedule.remove(8)
        NonCon_To_Schedule.remove(8)

        NonCon_To_Schedule.remove(choice1)
        NonCon_To_Schedule.remove(choice2)
        NonCon_To_Schedule.remove(choice3)

        # Find city teams the Concordia plays 
        dummy = [0,1,5,6]
        choice1 = random.choice(dummy)
        dummy.remove(choice1)
        choice2 = random.choice(dummy)
        dummy.remove(choice2)
        choice3 = random.choice(dummy)

        # Track teams that have to play each other
        NonCon_Left[3].append(choice1)
        NonCon_Left[3].append(choice2)
        NonCon_Left[3].append(choice3)

        NonCon_Left[choice1].append(3)
        NonCon_Left[choice2].append(3)
        NonCon_Left[choice3].append(3)

        NonCon_To_Schedule.remove(3)
        NonCon_To_Schedule.remove(3)
        NonCon_To_Schedule.remove(3)

        NonCon_To_Schedule.remove(choice1)
        NonCon_To_Schedule.remove(choice2)
        NonCon_To_Schedule.remove(choice3)

        # Finish Concordia opponent selection
        dummy = [2,4,9]
        choice1 = random.choice(dummy)
        dummy.remove(choice1)
        choice2 = random.choice(dummy)
        dummy.remove(choice2)

        NonCon_Left[3].append(choice1)
        NonCon_Left[3].append(choice2)

        NonCon_Left[choice1].append(3)
        NonCon_Left[choice2].append(3)

        NonCon_To_Schedule.remove(3)
        NonCon_To_Schedule.remove(3)

        NonCon_To_Schedule.remove(choice1)
        NonCon_To_Schedule.remove(choice2)

        # Finish Augsburg opponent selection
        # for loop to avoid bottlenecks
        for i in range(1,100):
            # if already have 6 opponents, move on
            if len(NonCon_Left[0]) == 6:
                break
            
            # Pick a team (if we can)
            choice = random.choice(NonCon_To_Schedule)
            
            if (choice == 0) or choice in  NonCon_Left[0]:
                pass
            
            else:
                NonCon_Left[0].append(choice)
                NonCon_Left[choice].append(0)
                NonCon_To_Schedule.remove(0)
                NonCon_To_Schedule.remove(choice)
                
            if i == 99:
                print("error - please re-run code")


        # Finish Bethel selection
        for i in range(1,100):
            if len(NonCon_Left[1]) == 6:
                break
            
            choice = random.choice(NonCon_To_Schedule)
            
            if (choice == 1) or choice in  NonCon_Left[1]:
                pass
            
            else:
                NonCon_Left[1].append(choice)
                NonCon_Left[choice].append(1)
                NonCon_To_Schedule.remove(1)
                NonCon_To_Schedule.remove(choice)
                

        # Finish Hamline selection
        for i in range(1,100):
            if len(NonCon_Left[5]) == 6:
                break
            
            choice = random.choice(NonCon_To_Schedule)
            
            if (choice == 5) or choice in  NonCon_Left[5]:
                pass
            
            else:
                NonCon_Left[5].append(choice)
                NonCon_Left[choice].append(5)
                NonCon_To_Schedule.remove(5)
                NonCon_To_Schedule.remove(choice)
            


        # Finish Hamline selection
        for i in range(1,100):
            if len(NonCon_Left[6]) == 6:
                break
            
            choice = random.choice(NonCon_To_Schedule)
            
            if (choice == 6) or choice in  NonCon_Left[6]:
                pass
            
            else:
                NonCon_Left[6].append(choice)
                NonCon_Left[choice].append(6)
                NonCon_To_Schedule.remove(6)
                NonCon_To_Schedule.remove(choice)
            


        # Finish Johns selection 
        for i in range(1,100):
            if len(NonCon_Left[7]) == 6:
                break
            
            choice = random.choice(NonCon_To_Schedule)
            
            if (choice == 7) or choice in  NonCon_Left[7]:
                pass
            
            else:
                NonCon_Left[7].append(choice)
                NonCon_Left[choice].append(7)
                NonCon_To_Schedule.remove(7)
                NonCon_To_Schedule.remove(choice)
            
    
        # Finalize selection for remaining teams
        for i in range(1,100):
            if len(NonCon_Left[2]) == 6:
                break
            
            choice = random.choice(NonCon_To_Schedule)
            
            if (choice == 2) or choice in  NonCon_Left[2]:
                pass
            
            else:
                NonCon_Left[2].append(choice)
                NonCon_Left[choice].append(2)
                NonCon_To_Schedule.remove(2)
                NonCon_To_Schedule.remove(choice)
            
    
        for i in range(1,100):
            if len(NonCon_Left[4]) == 6:
                break
            
            choice = random.choice(NonCon_To_Schedule)
            
            if (choice == 4) or choice in  NonCon_Left[4]:
                pass
            
            else:
                NonCon_Left[4].append(choice)
                NonCon_Left[choice].append(4)
                NonCon_To_Schedule.remove(4)
                NonCon_To_Schedule.remove(choice)
                
                
        for i in range(1,50):
            if len(NonCon_Left[9]) == 6:
                break
            
            choice = random.choice(NonCon_To_Schedule)
            
            if (choice == 9) or choice in  NonCon_Left[9]:
                pass
            
            else:
                NonCon_Left[9].append(choice)
                NonCon_Left[choice].append(9)
                NonCon_To_Schedule.remove(9)
                NonCon_To_Schedule.remove(choice)
                
        if len(NonCon_To_Schedule) == 0:
            return(NonCon_Left)
        
        if j > 99:
            print("error - please try again")
            
# Distance matrix that records the travel time between each school
dist_matrix = [
    # AUG BET CAR CON GAC HAM MAC SJU SMU STO CSS
    [0,	18,	50,	212, 72, 12, 13, 77, 126, 47, 142],  # Row 0 AUG
    [18	,	0	,	59	,	209	,	82	,	16	,	20	,	74	,	131	,	56	,	134],  # Row 1 BET
    [50	,	59	,	0	,	251	,	61	,	53	,	50	,	116	,	102	,	7	,	179],  # Row 2 CAR
    [212	,	209	,	251	,	0	,	258	,	217	,	218	,	142	,	330	,	248	,	255],  # Row 3 CON
    [72	,	82	,	61	,	258	,	0	,	79	,	77	,	123	,	137	,	59	,	206],  # Row 4 GAC
    [12	,	16	,	53	,	217	,	79	,	0	,	11	,	82	,	124	,	49	,	141],  # Row 5 HAM
    [13	,	20	,	50	,	218	,	77	,	11	,	0	,	84	,	125	,	47	,	143],  # Row 6 MAC
    [77	,	74	,	116	,	142	,	123	,	82	,	84	,	0	,	195	,	113	,	167],  # Row 7 SJU
    [126	,	131	,	102	,	330	,	137	,	124	,	125	,	195	,	0	,	105	,	229],  # Row 8 SMU
    [47	,	56	,	7	,	248	,	59	,	49	,	47	,	113	,	105	,	0	,	177],  # Row 9 STO
    [142	,	134	,	179	,	255	,	206	,	141	,	143	,	167	,	229	,	177	,	0]   # Row 10 CSS
]

# Make Schedule (specifically, iter of them)
for run in range(0,iter):
    schedule = schedule + 1
    
    # Try 1000 times (this will almost certainly be enough)
    MAX_RETRIES = 1000
    retry_count = 0

    while retry_count < MAX_RETRIES:
        try:


            # Track the week by week schedule
            Con_Sched = [[],
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

            # Track byes that need to be implemented
            Con_Bye_Track = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            # Pick non conference games using the function
            NonCon_Left = create_noncon()

            # We now schedule the non-conference games
            # for loop to avoid bottle necks
            for a in range(0,10):
                # Make week 1
                for k in range(0,25):
                    Can_Use = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    NonCon_Bye_Track = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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
                    []]

                    # Pick a team to be on bye
                    bye = random.choice(NonCon_Bye_Track)
                    Can_Use.remove(bye)

                    home = []
                    away = [] 
                    
                    # for loop to create 5 match ups for the 10 teams
                    for j in range(0, 5):
                                    
                        # Pick a team 
                        pick = random.choice(Can_Use)
                            
                        home.append(pick)
                        Can_Use.remove(pick)

                        # Find a valid opponent for the picked team
                        for i in range(0,100):
                            away_pick = random.choice(NonCon_Left[home[j]])
                            
                            # Check if we can use
                            if away_pick in Can_Use:
                                
                                away.append(away_pick)
                                Can_Use.remove(away_pick)
                                
                                break
                            
                            else:
                                pass
                    
                    # if we did get 5 matchups, move on
                    if len(away) == 5:
                        break
                    
                # if we did not get 5 matchups, try again
                if len(away) != 5:
                    pass
                
                # Tracking schedule and opponents remaining
                NonCon_Bye_Track.remove(bye)
                NonCon_Sched[bye].append(-1)
                    
                NonCon_Left[home[0]].remove(away[0])
                NonCon_Left[away[0]].remove(home[0])
                NonCon_Sched[home[0]].append(away[0])
                NonCon_Sched[away[0]].append(home[0])
                        
                NonCon_Left[home[1]].remove(away[1])
                NonCon_Left[away[1]].remove(home[1])
                NonCon_Sched[home[1]].append(away[1])
                NonCon_Sched[away[1]].append(home[1])

                NonCon_Left[home[2]].remove(away[2])
                NonCon_Left[away[2]].remove(home[2])
                NonCon_Sched[home[2]].append(away[2])
                NonCon_Sched[away[2]].append(home[2])
                        
                NonCon_Left[home[3]].remove(away[3])
                NonCon_Left[away[3]].remove(home[3])
                NonCon_Sched[home[3]].append(away[3])
                NonCon_Sched[away[3]].append(home[3])
                        
                NonCon_Left[home[4]].remove(away[4])
                NonCon_Left[away[4]].remove(home[4])
                NonCon_Sched[home[4]].append(away[4])
                NonCon_Sched[away[4]].append(home[4])

                NonCon_Bye_Track_Save = NonCon_Bye_Track
                NonCon_Sched_Save = NonCon_Sched


                # Make week 2 in the same way as we made week 1
                for k in range(0,25):
                    Can_Use = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    NonCon_Bye_Track = NonCon_Bye_Track_Save

                    NonCon_Sched = NonCon_Sched_Save

                    bye = random.choice(NonCon_Bye_Track)
                    Can_Use.remove(bye)

                    home = []
                    away = [] 
                    for j in range(0, 5):
                                    
                        # Pick a team 
                        pick = random.choice(Can_Use)
                            
                        home.append(pick)
                        Can_Use.remove(pick)

                        
                        for i in range(0,100):
                            away_pick = random.choice(NonCon_Left[pick])
                            
                            if away_pick in Can_Use:
                                
                                away.append(away_pick)
                                Can_Use.remove(away_pick)
                                
                                break
                    
                            

                            
                    if len(away) == 5:
                        break
                if len(away) != 5:
                    pass
                NonCon_Bye_Track.remove(bye)
                NonCon_Sched[bye].append(-1)

                NonCon_Left[home[0]].remove(away[0])
                NonCon_Left[away[0]].remove(home[0])
                NonCon_Sched[home[0]].append(away[0])
                NonCon_Sched[away[0]].append(home[0])
                        
                NonCon_Left[home[1]].remove(away[1])
                NonCon_Left[away[1]].remove(home[1])
                NonCon_Sched[home[1]].append(away[1])
                NonCon_Sched[away[1]].append(home[1])

                NonCon_Left[home[2]].remove(away[2])
                NonCon_Left[away[2]].remove(home[2])
                NonCon_Sched[home[2]].append(away[2])
                NonCon_Sched[away[2]].append(home[2])
                        
                NonCon_Left[home[3]].remove(away[3])
                NonCon_Left[away[3]].remove(home[3])
                NonCon_Sched[home[3]].append(away[3])
                NonCon_Sched[away[3]].append(home[3])
                        
                NonCon_Left[home[4]].remove(away[4])
                NonCon_Left[away[4]].remove(home[4])
                NonCon_Sched[home[4]].append(away[4])
                NonCon_Sched[away[4]].append(home[4])


                NonCon_Bye_Track_Save = NonCon_Bye_Track
                NonCon_Sched_Save = NonCon_Sched
                    
                # Make week 3
                for k in range(0,25):
                    Can_Use = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    NonCon_Bye_Track = NonCon_Bye_Track_Save

                    NonCon_Sched = NonCon_Sched_Save

                    bye = random.choice(NonCon_Bye_Track)
                    Can_Use.remove(bye)
                    
                    # Get three teams to be on bye this week
                    for i in range(0,100):
                        bye2 = random.choice(NonCon_Bye_Track)
                        if bye2 != bye:
                            Can_Use.remove(bye2)
                            break
                    
                    for i in range(0,100):
                        bye3 = random.choice(NonCon_Bye_Track)
                        if bye3 != bye and bye3 != bye2:
                            Can_Use.remove(bye3)
                            break
                    

                    home = []
                    away = [] 
                    for j in range(0, 4):
                                    
                        # Pick a team 
                        pick = random.choice(Can_Use)
                            
                        home.append(pick)
                        Can_Use.remove(pick)

                        
                        for i in range(0,100):
                            away_pick = random.choice(NonCon_Left[pick])
                            
                            if away_pick in Can_Use:
                                
                                away.append(away_pick)
                                Can_Use.remove(away_pick)
                                
                                break
                    
                            

                    # Checking if 4 matchups were made (as 3 teams are on bye)        
                    if len(away) == 4:
                        break
                if len(away) != 4:
                    pass        
                NonCon_Bye_Track.remove(bye)
                NonCon_Sched[bye].append(-1)
                NonCon_Bye_Track.remove(bye2)
                NonCon_Sched[bye2].append(-1)
                NonCon_Bye_Track.remove(bye3)
                NonCon_Sched[bye3].append(-1)

                NonCon_Left[home[0]].remove(away[0])
                NonCon_Left[away[0]].remove(home[0])
                NonCon_Sched[home[0]].append(away[0])
                NonCon_Sched[away[0]].append(home[0])
                        
                NonCon_Left[home[1]].remove(away[1])
                NonCon_Left[away[1]].remove(home[1])
                NonCon_Sched[home[1]].append(away[1])
                NonCon_Sched[away[1]].append(home[1])

                NonCon_Left[home[2]].remove(away[2])
                NonCon_Left[away[2]].remove(home[2])
                NonCon_Sched[home[2]].append(away[2])
                NonCon_Sched[away[2]].append(home[2])
                        
                NonCon_Left[home[3]].remove(away[3])
                NonCon_Left[away[3]].remove(home[3])
                NonCon_Sched[home[3]].append(away[3])
                NonCon_Sched[away[3]].append(home[3])


                NonCon_Bye_Track_Save = NonCon_Bye_Track
                NonCon_Sched_Save = NonCon_Sched
                    
                # Make week 4
                for k in range(0,25):
                    Can_Use = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    NonCon_Bye_Track = NonCon_Bye_Track_Save

                    NonCon_Sched = NonCon_Sched_Save

                    bye = random.choice(NonCon_Bye_Track)
                    Can_Use.remove(bye)

                    home = []
                    away = [] 
                    for j in range(0, 5):
                                    
                        # Pick a team 
                        pick = random.choice(Can_Use)
                            
                        home.append(pick)
                        Can_Use.remove(pick)

                        
                        for i in range(0,100):
                            away_pick = random.choice(NonCon_Left[pick])
                            
                            if away_pick in Can_Use:
                                
                                away.append(away_pick)
                                Can_Use.remove(away_pick)
                                
                                break
                    
                            

                            
                    if len(away) == 5:
                        break
                if len(away) != 5:
                    pass
                NonCon_Bye_Track.remove(bye)
                NonCon_Sched[bye].append(-1)

                NonCon_Left[home[0]].remove(away[0])
                NonCon_Left[away[0]].remove(home[0])
                NonCon_Sched[home[0]].append(away[0])
                NonCon_Sched[away[0]].append(home[0])
                        
                NonCon_Left[home[1]].remove(away[1])
                NonCon_Left[away[1]].remove(home[1])
                NonCon_Sched[home[1]].append(away[1])
                NonCon_Sched[away[1]].append(home[1])

                NonCon_Left[home[2]].remove(away[2])
                NonCon_Left[away[2]].remove(home[2])
                NonCon_Sched[home[2]].append(away[2])
                NonCon_Sched[away[2]].append(home[2])
                        
                NonCon_Left[home[3]].remove(away[3])
                NonCon_Left[away[3]].remove(home[3])
                NonCon_Sched[home[3]].append(away[3])
                NonCon_Sched[away[3]].append(home[3])
                        
                NonCon_Left[home[4]].remove(away[4])
                NonCon_Left[away[4]].remove(home[4])
                NonCon_Sched[home[4]].append(away[4])
                NonCon_Sched[away[4]].append(home[4])


                NonCon_Bye_Track_Save = NonCon_Bye_Track
                NonCon_Sched_Save = NonCon_Sched
                    
                    
                    # Make week 5 
                for k in range(0,25):
                    Can_Use = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    NonCon_Bye_Track = NonCon_Bye_Track_Save

                    NonCon_Sched = NonCon_Sched_Save

                    bye = random.choice(NonCon_Bye_Track)
                    Can_Use.remove(bye)

                    home = []
                    away = [] 
                    for j in range(0, 5):
                                    
                        # Pick a team 
                        pick = random.choice(Can_Use)
                            
                        home.append(pick)
                        Can_Use.remove(pick)

                        
                        for i in range(0,100):
                            away_pick = random.choice(NonCon_Left[pick])
                            
                            if away_pick in Can_Use:
                                
                                away.append(away_pick)
                                Can_Use.remove(away_pick)
                                
                                break
                    
                            

                            
                    if len(away) == 5:
                        break
                if len(away) != 5:
                    pass
                NonCon_Bye_Track.remove(bye)
                NonCon_Sched[bye].append(-1)

                NonCon_Left[home[0]].remove(away[0])
                NonCon_Left[away[0]].remove(home[0])
                NonCon_Sched[home[0]].append(away[0])
                NonCon_Sched[away[0]].append(home[0])
                        
                NonCon_Left[home[1]].remove(away[1])
                NonCon_Left[away[1]].remove(home[1])
                NonCon_Sched[home[1]].append(away[1])
                NonCon_Sched[away[1]].append(home[1])

                NonCon_Left[home[2]].remove(away[2])
                NonCon_Left[away[2]].remove(home[2])
                NonCon_Sched[home[2]].append(away[2])
                NonCon_Sched[away[2]].append(home[2])
                        
                NonCon_Left[home[3]].remove(away[3])
                NonCon_Left[away[3]].remove(home[3])
                NonCon_Sched[home[3]].append(away[3])
                NonCon_Sched[away[3]].append(home[3])
                        
                NonCon_Left[home[4]].remove(away[4])
                NonCon_Left[away[4]].remove(home[4])
                NonCon_Sched[home[4]].append(away[4])
                NonCon_Sched[away[4]].append(home[4])


                NonCon_Bye_Track_Save = NonCon_Bye_Track
                NonCon_Sched_Save = NonCon_Sched
                    
                    
                    
                # Make week 6 (3 teams on bye)
                for k in range(0,25):
                    Can_Use = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    NonCon_Bye_Track = NonCon_Bye_Track_Save

                    NonCon_Sched = NonCon_Sched_Save

                    bye = random.choice(NonCon_Bye_Track)
                    Can_Use.remove(bye)
                    
                
                    for i in range(0,100):
                        bye2 = random.choice(NonCon_Bye_Track)
                        if bye2 != bye:
                            Can_Use.remove(bye2)
                            break
                    
                    for i in range(0,100):
                        bye3 = random.choice(NonCon_Bye_Track)
                        if bye3 != bye and bye3 != bye2:
                            Can_Use.remove(bye3)
                            break
                    

                    home = []
                    away = [] 
                    for j in range(0, 4):
                                    
                        # Pick a team 
                        pick = random.choice(Can_Use)
                            
                        home.append(pick)
                        Can_Use.remove(pick)

                        
                        for i in range(0,100):
                            away_pick = random.choice(NonCon_Left[pick])
                            
                            if away_pick in Can_Use:
                                
                                away.append(away_pick)
                                Can_Use.remove(away_pick)
                                
                                break
                            
                    if len(away) == 4:
                        break
                    
                if len(away) != 4:
                    pass
                
                # Extra check for schedule validity
                if (away[0] not in NonCon_Left[home[0]]) or (away[1] not in NonCon_Left[home[1]]) or (away[2] not in NonCon_Left[home[2]]) :
                    pass
                
                NonCon_Bye_Track.remove(bye)
                NonCon_Sched[bye].append(-1)
                NonCon_Bye_Track.remove(bye2)
                NonCon_Sched[bye2].append(-1)
                NonCon_Bye_Track.remove(bye3)
                NonCon_Sched[bye3].append(-1)

                NonCon_Left[home[0]].remove(away[0])
                NonCon_Left[away[0]].remove(home[0])
                NonCon_Sched[home[0]].append(away[0])
                NonCon_Sched[away[0]].append(home[0])
                        
                NonCon_Left[home[1]].remove(away[1])
                NonCon_Left[away[1]].remove(home[1])
                NonCon_Sched[home[1]].append(away[1])
                NonCon_Sched[away[1]].append(home[1])

                NonCon_Left[home[2]].remove(away[2])
                NonCon_Left[away[2]].remove(home[2])
                NonCon_Sched[home[2]].append(away[2])
                NonCon_Sched[away[2]].append(home[2])
                        
                NonCon_Left[home[3]].remove(away[3])
                NonCon_Left[away[3]].remove(home[3])
                NonCon_Sched[home[3]].append(away[3])
                NonCon_Sched[away[3]].append(home[3])


                NonCon_Bye_Track_Save = NonCon_Bye_Track
                NonCon_Sched_Save = NonCon_Sched
                    
                    
                    
                # Make week 7
                for k in range(0,25):
                    Can_Use = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    NonCon_Bye_Track = NonCon_Bye_Track_Save

                    NonCon_Sched = NonCon_Sched_Save

                    bye = random.choice(NonCon_Bye_Track)
                    Can_Use.remove(bye)

                    home = []
                    away = [] 
                    for j in range(0, 5):
                                    
                        # Pick a team 
                        pick = random.choice(Can_Use)
                            
                        home.append(pick)
                        Can_Use.remove(pick)

                        
                        for i in range(0,100):
                            away_pick = random.choice(NonCon_Left[pick])
                            
                            if away_pick in Can_Use:
                                
                                away.append(away_pick)
                                Can_Use.remove(away_pick)
                                
                                break
                    
                            

                            
                    if len(away) == 5:
                        break
                if len(away) != 5:
                    pass
                
                # Extra check for schedule validity
                if (away[0] not in NonCon_Left[home[0]]) or (away[1] not in NonCon_Left[home[1]]) or (away[2] not in NonCon_Left[home[2]]) or (away[3] not in NonCon_Left[home[3]]) or (away[4] not in NonCon_Left[home[4]]):
                    pass
                
                NonCon_Bye_Track.remove(bye)
                NonCon_Sched[bye].append(-1)

                NonCon_Left[home[0]].remove(away[0])
                NonCon_Left[away[0]].remove(home[0])
                NonCon_Sched[home[0]].append(away[0])
                NonCon_Sched[away[0]].append(home[0])
                        
                NonCon_Left[home[1]].remove(away[1])
                NonCon_Left[away[1]].remove(home[1])
                NonCon_Sched[home[1]].append(away[1])
                NonCon_Sched[away[1]].append(home[1])

                NonCon_Left[home[2]].remove(away[2])
                NonCon_Left[away[2]].remove(home[2])
                NonCon_Sched[home[2]].append(away[2])
                NonCon_Sched[away[2]].append(home[2])
                        
                NonCon_Left[home[3]].remove(away[3])
                NonCon_Left[away[3]].remove(home[3])
                NonCon_Sched[home[3]].append(away[3])
                NonCon_Sched[away[3]].append(home[3])
                        
                NonCon_Left[home[4]].remove(away[4])
                NonCon_Left[away[4]].remove(home[4])
                NonCon_Sched[home[4]].append(away[4])
                NonCon_Sched[away[4]].append(home[4])

                NonCon_Bye_Track_Save = NonCon_Bye_Track
                NonCon_Sched_Save = NonCon_Sched
                break
                    
            # We now set home and away status for each scheduled non-con game
            # Set home and away (1 is home, 0 away, -1 is bye, 2 is a placeholder)
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
            [2,2,2,2,2,2,2]]

            # Teams to schedule for week
            teams_to_ha = [0,1,2,3,4,5,6,7,8,9,10]
            # pick a team
            based =  random.randint(0, 10)
            teams_to_ha.remove(based)

            rng = [0,0,0,1,1,1]
            
            # Bottleneck protection
            b = 0
                    
            # Pick home and away based on coin flip, checking if the team can have another home/away game
            for item in NonCon_Sched_Save[based]:
                
                # If on bye then make location be a bye
                if item == -1:
                    non_con_home_track[based][b] = -1
                    
                # If not on bye randomly assign home or away 
                else:
                    choice = random.choice(rng)
                    non_con_home_track[based][b] = choice
                    rng.remove(choice)
                    
                    # Set opponent location to match (i.e. be away if the team we picked was home)
                    non_con_home_track[item][b] = 1 - choice
                    
                b = b + 1

            # Repeat process for the rest of the teams
            for c in range(0,10):
                based = random.choice(teams_to_ha)
                teams_to_ha.remove(based)

                rng = [0,0,0,1,1,1]

                for item in non_con_home_track[based]:
                    if item == 0:
                        rng.remove(0)
                    if item == 1:
                        rng.remove(1)

                b = 0

                for item in NonCon_Sched_Save[based]:
                    
                    if (non_con_home_track[based][b] == 1) or (non_con_home_track[based][b] == 0):
                        b = b + 1
                        
                    
                    elif item == -1:
                        # track schedule
                        non_con_home_track[based][b] = -1
                        b = b + 1
                        
                    else:
                        
                        choice = random.choice(rng)
                        
                        # track schedule
                        non_con_home_track[based][b] = choice
                        rng.remove(choice)
                        
                        non_con_home_track[item][b] = 1 - choice
                        b = b + 1
                            

            # Now we schedule the conference games
            for a in range(0, 10):
                
            # Track who we still need to play for each (round robin)
                Left = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                [0, 1, 3, 4, 5, 6, 7, 8, 9, 10],
                [0, 1, 2, 4, 5, 6, 7, 8, 9, 10],
                [0, 1, 2, 3, 5, 6, 7, 8, 9, 10],
                [0, 1, 2, 3, 4, 6, 7, 8, 9, 10],
                [0, 1, 2, 3, 4, 5, 7, 8, 9, 10],
                [0, 1, 2, 3, 4, 5, 6, 8, 9, 10],
                [0, 1, 2, 3, 4, 5, 6, 7, 9, 10],
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]

                # Track the week by week schedule
                Sched = [[],
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

                # Each team will need a bye
                Bye_Track = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            # For each week
                for k in range(1,12):
                    
                    # Pick a team to be on bye
                    bye = random.choice(Bye_Track)
                    
                    Bye_Track.remove(bye)
                    
                    # Track that this team is on bye
                    Sched[bye].append(-1)

                    # Loop till accurate week (bottleneck protection)
                    for l in range(0,250):
                        Can_Use = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                        Can_Use.remove(bye)

                        home = []
                        away = [] 
                        
                        # For each of 5 games
                        for j in range(0, 5):
                            
                            # Pick a team 
                            pick = random.choice(Can_Use)
                                
                            home.append(pick)
                            Can_Use.remove(home[j])
                    
                            # Pick a valid opponent
                            for i in range(0,100):
                                away_pick = random.choice(Left[home[j]])
                                
                                if away_pick in Can_Use:
                                    
                                    away.append(away_pick)
                                    Can_Use.remove(away_pick)
                                    
                                    break
                                
                                else:
                                    pass
                        # If we have matched up 5 pairs of teams move on
                        if len(away) == 5:     
                            break
                        # Otherwise try again
                        else:
                            pass   
                                
                    # Update home list
                    if len(away) != 5:     
                        break
                    
                    # Bottleneck protection
                    if a > 8:
                        print("error - try again")

                    # Track games that need to be scheduled and the scheduled games
                    Left[home[0]].remove(away[0])
                    Left[away[0]].remove(home[0])
                    Sched[home[0]].append(away[0])
                    Sched[away[0]].append(home[0])
                    
                    Left[home[1]].remove(away[1])
                    Left[away[1]].remove(home[1])
                    Sched[home[1]].append(away[1])
                    Sched[away[1]].append(home[1])

                    Left[home[2]].remove(away[2])
                    Left[away[2]].remove(home[2])
                    Sched[home[2]].append(away[2])
                    Sched[away[2]].append(home[2])
                    
                    Left[home[3]].remove(away[3])
                    Left[away[3]].remove(home[3])
                    Sched[home[3]].append(away[3])
                    Sched[away[3]].append(home[3])
                    
                    Left[home[4]].remove(away[4])
                    Left[away[4]].remove(home[4])
                    Sched[home[4]].append(away[4])
                    Sched[away[4]].append(home[4])
                    
                if len(Sched[0]) ==  len(Sched[1]) == 11:
                    break
                    
                    
            # Figure out home and away for conference games (2 is again a placeholder)
            home_track = [[2,2,2,2,2,2,2,2,2,2,2],
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


            # Flip location from non conference games for repeat matchups
            # for team
            for z in range(0,11):
                # for possible opponent
                for w in range(0,11):
                    if w in NonCon_Sched_Save[z]:
                        # Find the locale and swap it
                        non_con_when = NonCon_Sched_Save[z].index(w)
                        z_locale = non_con_home_track[z][non_con_when]
                        
                        ind = Sched[z].index(w)
                        
                        home_track[z][ind] = 1 - z_locale
                        

            # List of teams
            teams_to_ha = [0,1,2,3,4,5,6,7,8,9,10]

            # For each team number
            for c in range(0,11):
                
                # Pick a team
                based = random.choice(teams_to_ha)
                teams_to_ha.remove(based)

                # Need 5 home and 5 away
                rng = [0,0,0,0,0,1,1,1,1,1]

                # remove instances of a team already playing home/away due to non-con games
                for item in home_track[based]:
                    if item == 0:
                        rng.remove(0)
                    if item == 1:
                        rng.remove(1)

                # bottleneck protection
                b = 0


                for item in Sched[based]:
                    
                    # if already scheduled move on
                    if (home_track[based][b] == 1) or (home_track[based][b] == 0):
                        b = b + 1
                        
                    # If a bye record that in the home/away list and move on
                    elif item == -1:
                        home_track[based][b] = -1
                        b = b + 1
                        

                    # Otherwise, randomally select a locale
                    else:
                        
                        choice = random.choice(rng)
                        
                        home_track[based][b] = choice
                        rng.remove(choice)
                        
                        home_track[item][b] = 1 - choice
                        b = b + 1
    
            break 
        
        
        # If we fail 999 times break (this will almost never occur)
        except:
            retry_count += 1
            print(f"Retry {retry_count}/{MAX_RETRIES}...")
            
            if retry_count > 998:
                print("This is rare! We failed to make a schedule 999 times in a row! Please try again.")
            
            
    # Schedule is made, output to a CSV
    Full_Schedule = [[],[],[],[],[],[],[],[],[],[],[]]

    for p in range (0,11):
        Full_Schedule[p] = [schedule, NonCon_Sched_Save[p][0], non_con_home_track[p][0], distance(p, NonCon_Sched_Save[p][0]),
                            Sched[p][0],             home_track[p][0],         distance(p, Sched[p][0]),
                            NonCon_Sched_Save[p][1], non_con_home_track[p][1], distance(p, NonCon_Sched_Save[p][1]),
                            Sched[p][1],             home_track[p][1],         distance(p, Sched[p][1]),
                            NonCon_Sched_Save[p][2], non_con_home_track[p][2], distance(p, NonCon_Sched_Save[p][2]),
                            Sched[p][2],             home_track[p][2],         distance(p, Sched[p][2]),
                            NonCon_Sched_Save[p][3], non_con_home_track[p][3], distance(p, NonCon_Sched_Save[p][3]),
                            Sched[p][3],             home_track[p][3],         distance(p, Sched[p][3]),
                            Sched[p][4],             home_track[p][4],         distance(p, Sched[p][4]),
                            Sched[p][5],             home_track[p][5],         distance(p, Sched[p][5]),
                            NonCon_Sched_Save[p][4], non_con_home_track[p][4], distance(p, NonCon_Sched_Save[p][4]),
                            Sched[p][6],             home_track[p][6],         distance(p, Sched[p][6]),
                            NonCon_Sched_Save[p][5], non_con_home_track[p][5], distance(p, NonCon_Sched_Save[p][5]),
                            Sched[p][7],             home_track[p][7],         distance(p, Sched[p][7]),
                            Sched[p][8],             home_track[p][8],         distance(p, Sched[p][8]),
                            Sched[p][9],             home_track[p][9],         distance(p, Sched[p][9]),
                            NonCon_Sched_Save[p][6], non_con_home_track[p][6], distance(p, NonCon_Sched_Save[p][6]),
                            Sched[p][10],             home_track[p][10],       distance(p, Sched[p][10])]

    # Output
    with open('CompletedSchedule.csv', 'a') as f:
        writer = csv.writer(f)
        for item in Full_Schedule:
            writer.writerow(item)   