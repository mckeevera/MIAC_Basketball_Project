# MIAC_Basketball_Project
Code and documents for Alex McKeever's project working on creating MIAC Basketball schedules. Created for Ryan Kershaw and Katie St. Clair.

Contact: alexmckeever25@gmail.com

There are three different schedule ideas notated as V1, V2, and V3. The specifics of each schedule and an outline of their creation process are detailed below. Additionally, presentations for V1 and V3 exist that explain things more in depth as well regarding schedule metrics. We shifted away from V2 early in development and hence it lacks a presentation.

# Directory

## V1 - Men 10 Con/6 Noncon
This version of the schedule is one that creates a 16 game schedule. Each Men's team plays every other team once in a conference game and then 6 repeat opponents in a non-conference game. These games are interspersed throughout a 18 round schedule with each team getting one conference bye round and one non-conference bye round. We begin by selecting the 6 repeat opponents for each team based on some element of randomness while fixing some matchups. That is, we ensure games like Carleton-Olaf happen due to geographical location. We then assign all of the games to create a 16 round schedule and set a location for each. For repeat matchups the location is always different (i.e. Carleton would be at home for one game against Olaf, and away for one). Each team has 5 home and 5 away conference games and 3 home and 3 away non-conference games.

Metrics regarding how good a schedule is, based upon things like the number of home or away games in a row or distance traveled, are computed in the Rmd files. We then filter to some of the best schedules based on these "fairness" and "goodness" metrics gaining several candidate schedules detailed in the presentation.

### CSVs
- ScheduleSet1.csv through ScheduleSet6.csv - Mass produced schedules with each row corresponding to one team. A set of 11 rows therefore makes up a whole schedule. Variables include a team's opponent for each round as well as the location of the game and how far the team must travel. Due to storage constraints, these files are housed here: https://drive.google.com/drive/folders/1Nlhw3opZYIgBc8vQEVJVk-ts7mLRLEJ2?usp=sharing
- FilteredSet1.csv through FilteredSet17.csv - Filtered from ScheduleSet1.csv through ScheduleSet6.csv, these schedules are filtered such that back to back matchup repeats and back to back byes do not occur. These are then further analyzed in the Rmd files.

### Presentations
- Crafting a New MIAC Basketball Schedule.pdf - Presentation detailing the V1 methodology as well as canidate schedules. The math behind various metrics, such as a Team Pain score, are included as well.
  
### RMDs
- Filter.Rmd - Loads raw schedules and computes various metrics relating to the number of rounds between byes or repeat matchups. Filters are then used to remove unwanted schedules based on these metrics.
- Metrics.Rmd - Computation of average metrics related to travel distance and Team Pain for each team based on schedules. These are used as baseline numbers to analyze how good or bad a schedule is as it helps condition on the fact that teams like Scholastica will naturally have a harder schedule due to geography.
- Selection.Rmd - Takes the filtered schedules from Filter.Rmd and, in tandem with the metrics computed in Metrics.Rmd, further analyzes schedules. Based on filters looking at distance and Team Pain "fairness" and "goodness" we filter to 6 candidate schedules.
- Visualization.Rmd - Creation of the histograms/density plots used in the presentation. These plots showcase how good a schedule is compared to one that is randomaly generated on the basis of distance and Team Pain "fairness" and "goodness."
  
### Schedule_Maker
- MakeSchedule1.py - Code used to generate a schedule for V1. It will create schedules repeatedly until it reaches a chosen max iteration number.

## V2 - Men/Women Con/Noncon
This version of the schedule includes schedules for both the Men and Women. They are paired schedules with the Men's being a subset of the Women's with St. Kate's acting as a bye week for Men. The Men play 10 conference games and 8 repeat non-conference opponents while the Women play 11 conference games and 7 repeat non-conference opponents. The schedules are generated similarly to V1 with first a somewhat randomized selection of the repeat games before the scheduling and location of the games are set. Extra computations also compute where an extra Men's team bye must take place to ensure each Men's team gets 2 bye rounds.

### Schedule_Maker
- MakeSchedule2.py - Code used to generate a schedule for V2.

## V3 - Men/Women 18 Con
The final iteration of the schedule includings 18 conference games for Men and Women. Naturally, this means that Men will play a round robin and then 8 extra games and the Women will play a round robin and 7 extra games. We begin by determining the repeat opponents based on distance and some element of randomness for the Men, taking a subset of these repeat opponents for the Women's repeat opponents. We then assign locations for these matchups in such a way that ensures even splits. We then schedule the round robin games on saturdays (as well as the first two weekday rounds to help the math work out) as double headers for Men and Women assigning locations that are opposite of the repeat games if applicable. We then schedule the repeat games (not forced to be double headers) in such a way the back to back repreat batchups do not occur. Some metrics regarding distance and home/away streaks are then calculated for the schedule to avoid having to use RAM intensive procedures in R.

### CSVs
- ScheduleSet1.csv through ScheduleSet3.csv - Mass produced schedules with each row corresponding to one team and one gender. Hence, 23 row sets correspond to one full MIAC schedule. Variables include opponents, distance, and location, along with total traveled distance and the length between repeat opponents as well as home/away streak counts. These schedules are analyzed in MetricExtract.Rmd.

### Presentations
- MIAC BASKETBALL SCHEDULE PROJECT (18 Conference Games).pdf -  Presentation detailing the V3 methodology as well as canidate schedules. The math behind various metrics, such as a Team Pain score, are included as well. 
  
### RMDs
- MetricExtract.Rmd - Code used to calculate metrics and analyze the V3 schedules. Additionally, graphics correspond to how "good" or "fair" a schedule is are produced as well.
  
### Schedule_Maker
- MakeSchedule3.py - Code used to generate a schedule for V3. It will create schedules repeatedly until stopped.
