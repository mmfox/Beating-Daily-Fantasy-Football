import nflgame
import datetime
import csv
from enum import Enum

# Enumerated type for player position
Position = Enum('Position', 'WR QB RB')

#######################################################################################
#
# Helper Function definitions
#
######################################################################################

# Function which finds player from a given player list
def findPlayerById(player_list, pid):
    for p in player_list:
        lastp = p
        if(p.playerid == pid):
            return (1, p)
    # If we didn't find the player, return some valid player
    return (0, lastp)

# Function to build up data for a given player for a given week
def populate_data(yr, wk, pid, pos_id):
    points = []    
    points.append(getFantasyPoints(1, pid))
    points.append(getFantasyPoints(2, pid))
    points.append(getFantasyPoints(3, pid))
    points.append(getFantasyPoints(4, pid))
    points.append(getFantasyPoints(5, pid))
    points.append(getFantasyPoints(6, pid))

    # We want to leave out the most recent week that a player didn't get any points
    # This should hopefully remove bye weeks (without a schedule and player-team mapping)
    # Decide which week to leave out - default to the sixth week (index 5)
    leave_out_week = 5
    for i in range(0,6):
       if(points[i] == 0):
           leave_out_week = i
           break 

    # Calculate points scored for 1, 3, and 5 game sliding windows  
    added = 0
    points3 = 0
    points5 = 0
    for i in range(0,6):
        if(i != leave_out_week):
            if(added < 1):
               points1 = points[i];
            if(added < 3):
               points3 = points3 + points[i]
            if(added < 5):
               points5 = points5 + points[i]
            added = added + 1

    # Get correct windows of player statistics
    last_1_games_total_stats = players_1[leave_out_week]
    last_3_games_total_stats = players_3[leave_out_week]
    last_5_games_total_stats = players_5[leave_out_week]

    # Pull this player's specific stats from these game windows
    (p1_present, player_1_games_stats) = findPlayerById(last_1_games_total_stats, pid)
    (p3_present, player_3_games_stats) = findPlayerById(last_3_games_total_stats, pid)
    (p5_present, player_5_games_stats) = findPlayerById(last_5_games_total_stats, pid)

    # Now let's populate the data for the correct position
    if(pos_id == Position.WR):
       populate_wr_data(yr, wk, player_1_games_stats, player_3_games_stats, player_5_games_stats, points1, points3, points5, pid)
    elif(pos_id == Position.RB):
       populate_rb_data(yr, wk, player_1_games_stats, player_3_games_stats, player_5_games_stats, points1, points3, points5, pid)
    elif(pos_id == Position.QB):
       populate_qb_data(yr, wk, player_1_games_stats, player_3_games_stats, player_5_games_stats, points1, points3, points5, pid)

# This function fills in the global WR DATA array with the feature variables 
def populate_wr_data(yr, wk, p1, p3, p5, points1, points3, points5, pid): 
    global WR_DATA
    local_wr_data = []
    local_wr_data = [p1.receiving_yds, p1.receiving_tds, p1.receiving_rec, points1, p3.receiving_yds, p3.receiving_tds, p3.receiving_rec, points3, p5.receiving_yds, p5.receiving_tds, p5.receiving_rec, points5]
    actual_points = getFantasyPoints(0, pid)
    local_wr_data.append(actual_points)
    # We only want to look at players who actually played this week 
    # By filtering out 0 point performances, we hope to remove injured players
    # And players who are on a bye week
    if(actual_points > 0):
        WR_DATA.append(local_wr_data)

# This function fills in the global QB DATA array with the feature variables
def populate_qb_data(yr, wk, p1, p3, p5, points1, points3, points5, pid):
    global QB_DATA
    local_qb_data = [p1.passing_yds, p1.passing_tds, p1.passing_att, p1.passing_cmp, p1.passing_ints, points1, p3.passing_yds, p3.passing_tds, p3.passing_att, p3.passing_cmp, p3.passing_ints, points3, p5.passing_yds, p5.passing_tds, p5.passing_att, p5.passing_cmp, p5.passing_ints, points5]
    actual_points = getFantasyPoints(0, pid)
    local_qb_data.append(actual_points)
    # Again filter out 0 point performances to get rid of injuries and bye weeks
    if(actual_points > 0):
        QB_DATA.append(local_qb_data)

# This function fills in the global RB DATA array with the feature variables
def populate_rb_data(yr, wk, p1, p3, p5, points1, points3, points5, pid):
    global RB_DATA
    # Receiving stats are important for running back prediction.  However, the data
    # set used doesn't always have the prpoer data if there were not receiving stats.  
    # Therefore, clean up the data with the following code
    if 'receiving_yds' not in p1.__dict__:
        p1.receiving_yds = 0
        p1.receiving_tds = 0
        p1.receiving_rec = 0
    if 'receiving_yds' not in p3.__dict__:
        p3.receiving_yds = 0
        p3.receiving_tds = 0
        p3.receiving_rec = 0
    if 'receiving_yds' not in p5.__dict__:
        p5.receiving_yds = 0
        p5.receiving_tds = 0
        p5.receiving_rec = 0

    local_rb_data = [p1.rushing_yds, p1.rushing_tds, p1.rushing_att, p1.receiving_yds, p1.receiving_tds, p1.receiving_rec, points1, p3.rushing_yds, p3.rushing_tds, p3.rushing_att, p3.receiving_yds, p3.receiving_tds, p3.receiving_rec, points3, p5.rushing_yds, p5.rushing_tds, p5.rushing_att, p5.receiving_yds, p5.receiving_tds, p5.receiving_rec, points5]
    actual_points = getFantasyPoints(0, pid)
    local_rb_data.append(actual_points)
    # Again filter out 0 point performancs to get rid of injuries and bye weeks
    if(actual_points > 0):
        RB_DATA.append(local_rb_data)

# Function to get fantasy points for a player from a variable number of prior weeks 
def getFantasyPoints(wk, pid):
    # Default points to 0 in case this player is not in this week's data 
    points = 0
   
    # There are different data structures for the current week and previous weeks
    if(wk == 0):
        (player_exists, p) = findPlayerById(curr_week, pid)
    else:
        (player_exists, p) = findPlayerById(players[wk-1], pid)

    # Calculate fantasy points from DraftKings fantasy scoring procedure if we found the player
    # Guard each section with a local variable that will only be present if data is clean
    if(player_exists):
        if 'passing_yds' in p.__dict__:
            points += p.passing_tds * 4 + p.passing_yds * 0.04 - p.passing_ints + p.passing_twoptm * 2
            if(p.passing_yds >= 300):
               points += 3
        if 'rushing_yds' in p.__dict__:
            points += p.rushing_tds * 6 + p.rushing_yds * 0.1 + p.rushing_twoptm * 2
            if(p.rushing_yds >= 100):
               points += 3
        if 'receiving_yds' in p.__dict__:
            points += p.receiving_tds * 6 + p.receiving_yds * 0.1 + p.receiving_rec + p.receiving_twoptm * 2
            if(p.receiving_yds >= 100):
               points += 3
    return points


#######################################################################################
#
# Main script flows
#
######################################################################################

# Since this script takes awhile to run, print out the start time to the terminal for 
# benchmarking purposes
current_time = datetime.datetime.now().time()
print "Time Started \n"
print current_time.isoformat()
print "\n"

# Setup some global variables that will be used throughout the script
global games     # Array of game stats from the past 6 weeks 
global players_1 # Array of game stats from the past week (indexed by the week that will be left out for calculations) 
global players_3 # Array of game stats from the past 3 weeks (indexed by the week that will be left out for calculations)
global players_5 # Array of game stats from the past 5 weeks (indexed by the week that will be left ouf for calcuiations)
global curr_week # Current week player stats 
global players   # Array of player stats from the past 6 weeks
WR_DATA = []     # Final array of wr data plus actual fantasy points
RB_DATA = []     # Final array of rb data plus actual fantasy points
QB_DATA = []     # Final array of qb data plus actual fantasy points
games = []
players_1 = []
players_3 = []
players_5 = []
curr_week = []

# Loop over all of the relevant weeks that we are using for the algorithm
for year in xrange(2016, 2017):
    for local_week in xrange(7, 15):
        # Print out some checkpointing for performance monitoring
        print "Year " + repr(year) + " Week " + repr(local_week)

        # Reset week-dependent global variables
        players = []
        games = []
        curr_week = []

        # Update current week player stats
        curr_week_games = nflgame.games(year, week=local_week)
        curr_week = nflgame.combine_game_stats(curr_week_games)

        # Add all game stats to our games global variable
        for i in xrange(1,7):
           games.append(nflgame.games(year, week=local_week-i))

        # Grab player stats from game stats
        for i in xrange(0,6):
           players.append(nflgame.combine_game_stats(games[i]))

        # Last 3 games' player stats is commonly needed, so merge data ahead of time
        combo_3_games = games[0] + games[1] + games[2]
        players_last_3 = nflgame.combine_game_stats(combo_3_games);

        # Create all needed permutations of 1, 3, and 5 game windows (indexed by week left out)
        for i in xrange(0,6):
            if(i != 0):
                players_1.append(players[0])
            else:     
                players_1.append(players[1])

            if(i < 3):
                local_g = []
                for j in range(0,3):
                    if(j != i):
                       local_g += games[j]
                players_3.append(nflgame.combine_game_stats(local_g))
            else:
                players_3.append(players_last_3)
  
            local_g6 = []
            for j in range(0,6):
                if(j != i):
                    local_g6 += games[j]
            players_5.append(nflgame.combine_game_stats(local_g6))

        print "Combined games"

        # For each week, only select players who have been at the top of their position 
        # group over the last 3 played games (and who have played in one of the last two games)
        for p3 in players_last_3.receiving().sort('receiving_yds').limit(60):
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players[0], pid)
            if(p1_present == 0):
                (p1_present, p1) = findPlayerById(players[1], pid)
            if(p1_present):
                populate_data(year, local_week, pid, Position.WR)
        for p3 in players_last_3.passing().sort('passing_yds').limit(25):
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players[0], pid)
            if(p1_present == 0):
                (p1_present, p1) = findPlayerById(players[1], pid)
            if(p1_present):
                populate_data(year, local_week, pid, Position.QB)
        for p3 in players_last_3.rushing().sort('rushing_yds').limit(25):
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players[0], pid)
            if(p1_present == 0):
                (p1_present, p1) = findPlayerById(players[1], pid)
            if(p1_present):
                populate_data(year, local_week, pid, Position.RB)

# Write out data to CSV files to be consumed by MatLab Machine Learning algorithms
print "Writing WR data"
with open('wr_test_data.csv', 'wb') as wr_csvfile:
    wr_writer = csv.writer(wr_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(WR_DATA)):
        wr_writer.writerow(WR_DATA[i])

print "Writing RB data"
with open('rb_test_data.csv', 'wb') as rb_csvfile:
    rb_writer = csv.writer(rb_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(RB_DATA)):
        rb_writer.writerow(RB_DATA[i])

print "Writing QB data"
with open('qb_test_data.csv', 'wb') as qb_csvfile:
    qb_writer = csv.writer(qb_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(QB_DATA)):
        qb_writer.writerow(QB_DATA[i])


current_time = datetime.datetime.now().time()
print "Finished choosing players to analyze and gathering their features."
print current_time.isoformat()


