# MIAC_Basketball_Project
Code and documents for Alex McKeever's project working on creating MIAC Basketball schedules. Supported by Ryan Kershaw and Katie St. Clair.

Contact: alexmckeever25@gmail.com

There are three different schedule ideas notated as V1, V2, and V3. The specifics of each schedule and an outline of their creation process are detailed below. Additionally, presentations for V1 and V3 exist that explain things more in depth as well regarding schedule metrics. We shifted away from V2 early in development and hence it lacks a presentation.

# Directory

## V1 - Men 10 Con/6 Noncon
This version of the schedule is one that creates a 16 game schedule. Each Men's team plays every other team once in a conference game and then 6 repeat opponents in a non-conference game. These games are interspersed throughout a 18 round schedule with each team getting one conference bye round and one non-conference bye round. We begin by selecting the 6 repeat opponents for each team

Metrics regarding how good a schedule is are computed 

### CSVs
- ScheduleSet1.csv through ScheduleSet6.csv - with each column representing
- https://drive.google.com/drive/folders/1Nlhw3opZYIgBc8vQEVJVk-ts7mLRLEJ2?usp=sharing
- FilteredSet1.csv through FilteredSet17.csv - 

### Presentations
- Crafting a New MIAC Basketball Schedule.pdf -
  
### RMDs
- Filter.Rmd - 
- Metrics.Rmd - 
- Selection.Rmd - 
- Visualization.Rmd - 
  
### Schedule_Maker
- MakeSchedule1.py - Code used to generate a schedule for V1. It will create schedules repeatedly until it reaches a chosen max iteration number.

## V2 - Men/Women Con/Noncon
This version of the schedule includes schedules for both the Men and Women. They are paired schedules...

### Schedule_Maker
- MakeSchedule2.py - Code used to generate a schedule for V2.

## V3 - Men/Women 18 Con

### CSVs
- ScheduleSet1.csv through ScheduleSet3.csv - with each column representing

### Presentations
- MIAC BASKETBALL SCHEDULE PROJECT (18 Conference Games).pdf -
  
### RMDs
- MetricExtract.Rmd
  
### Schedule_Maker
- MakeSchedule3.py - Code used to generate a schedule for V3. It will create schedules repeatedly until stopped.
