import nflgame
import datetime
import csv

def findPlayerById(player_list, pid):
    for p in player_list:
        lastp = p
        if(p.playerid == pid):
            return (1, p)
    return (0, lastp)

def populate_data(yr, wk, pid, pos_id):
    points = []
    leave_out_week = 5
    points.append(getFantasyPoints(1, pid))
    points.append(getFantasyPoints(2, pid))
    points.append(getFantasyPoints(3, pid))
    points.append(getFantasyPoints(4, pid))
    points.append(getFantasyPoints(5, pid))
    points.append(getFantasyPoints(6, pid))
    for i in range(0,6):
       if(points[i] == 0):
           leave_out_week = i
           break 
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
    play1 = players_1[leave_out_week]
    play3 = players_3[leave_out_week]
    play5 = players_5[leave_out_week]
    (p1_present, p1) = findPlayerById(play1, pid)
    (p3_present, p3) = findPlayerById(play3, pid)
    (p5_present, p5) = findPlayerById(play5, pid)
    if(pos_id == 0):
       populate_wr_data(yr, wk, p1, p3, p5, points1, points3, points5, pid)
    elif(pos_id == 1):
       populate_rb_data(yr, wk, p1, p3, p5, points1, points3, points5, pid)
    else:
       populate_qb_data(yr, wk, p1, p3, p5, points1, points3, points5, pid)

def populate_wr_data(yr, wk, p1, p3, p5, points1, points3, points5, pid): 
    global WR_DATA
    local_wr_data = []
    local_wr_data = [p1.receiving_yds, p1.receiving_tds, p1.receiving_rec, points1, p3.receiving_yds, p3.receiving_tds, p3.receiving_rec, points3, p5.receiving_yds, p5.receiving_tds, p5.receiving_rec, points5]
    actual_points = getFantasyPoints(0, pid)
    local_wr_data.append(actual_points)
    if(actual_points > 0):
        WR_DATA.append(local_wr_data)


def populate_qb_data(yr, wk, p1, p3, p5, points1, points3, points5, pid):
    global QB_DATA
    local_qb_data = [p1.passing_yds, p1.passing_tds, p1.passing_att, p1.passing_cmp, p1.passing_ints, points1, p3.passing_yds, p3.passing_tds, p3.passing_att, p3.passing_cmp, p3.passing_ints, points3, p5.passing_yds, p5.passing_tds, p5.passing_att, p5.passing_cmp, p5.passing_ints, points5]
    actual_points = getFantasyPoints(0, pid)
    local_qb_data.append(actual_points)
    if(actual_points > 0):
        QB_DATA.append(local_qb_data)


def populate_rb_data(yr, wk, p1, p3, p5, points1, points3, points5, pid):
    global RB_DATA
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
    if(actual_points > 0):
        RB_DATA.append(local_rb_data)


def getFantasyPoints(wk, pid):
    points = 0
    if(wk == 0):
        (player_exists, p) = findPlayerById(curr_week, pid)
    elif(wk == 1):
        (player_exists, p) = findPlayerById(players[0], pid)
    elif(wk == 2):
        (player_exists, p) = findPlayerById(players[1], pid)
    elif(wk == 3):
        (player_exists, p) = findPlayerById(players[2], pid)
    elif(wk == 4):
        (player_exists, p) = findPlayerById(players[3], pid)
    elif(wk == 5):
        (player_exists, p) = findPlayerById(players[4], pid)
    else:
        (player_exists, p) = findPlayerById(players[5], pid)

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

current_time = datetime.datetime.now().time()
print "Time Started \n"
print current_time.isoformat()
print "\n"

global games
global players_1
global players_3
global players_5
global curr_week
global players
WR_DATA = []
RB_DATA = []
QB_DATA = []
games = []
players_1 = []
players_3 = []
players_5 = []
curr_week = []

for year in range(2009, 2016):
    for local_week in range(7, 17):
        print "Year " + repr(year) + " Week " + repr(local_week)
        players = []
        games = []
        curr_week = []
        curr_week_games = nflgame.games(year, week=local_week)
        curr_week = nflgame.combine_game_stats(curr_week_games)

        games.append(nflgame.games(year, week=local_week-1))
        games.append(nflgame.games(year, week=local_week-2))
        games.append(nflgame.games(year, week=local_week-3))
        games.append(nflgame.games(year, week=local_week-4))
        games.append(nflgame.games(year, week=local_week-5))
        games.append(nflgame.games(year, week=local_week-6))
        combo_3_games = games[0] + games[1] + games[2]
        players.append(nflgame.combine_game_stats(games[0]))
        players.append(nflgame.combine_game_stats(games[1]))
        players.append(nflgame.combine_game_stats(games[2]))
        players.append(nflgame.combine_game_stats(games[3]))
        players.append(nflgame.combine_game_stats(games[4]))
        players.append(nflgame.combine_game_stats(games[5]))
        players_last_3 = nflgame.combine_game_stats(combo_3_games);
        print "Combined games"

        #Create all needed permutations
        for i in range(0,6):
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
        print "Truly combined games"


        for p3 in players_last_3.receiving().sort('receiving_yds').limit(60):
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players[0], pid)
            if(p1_present == 0):
                (p1_present, p1) = findPlayerById(players[1], pid)
            if(p1_present):
                #print "Working on WR " + p3.name
                populate_data(year, local_week, pid, 0)
        for p3 in players_last_3.passing().sort('passing_yds').limit(25):
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players[0], pid)
            if(p1_present == 0):
                (p1_present, p1) = findPlayerById(players[1], pid)
            if(p1_present):
                #print "Working on QB " + p3.name
                populate_data(year, local_week, pid, 2)
        for p3 in players_last_3.rushing().sort('rushing_yds').limit(25):
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players[0], pid)
            if(p1_present == 0):
                (p1_present, p1) = findPlayerById(players[1], pid)
            if(p1_present):
                #print "Working on RB " + p3.name
                populate_data(year, local_week, pid, 1)


print "Writing WR data"
with open('wr_data_cp.csv', 'wb') as wr_csvfile:
    wr_writer = csv.writer(wr_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(WR_DATA)):
        wr_writer.writerow(WR_DATA[i])

print "Writing RB data"
with open('rb_data_cp.csv', 'wb') as rb_csvfile:
    rb_writer = csv.writer(rb_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(RB_DATA)):
        rb_writer.writerow(RB_DATA[i])

print "Writing QB data"
with open('qb_data_cp.csv', 'wb') as qb_csvfile:
    qb_writer = csv.writer(qb_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(QB_DATA)):
        qb_writer.writerow(QB_DATA[i])


current_time = datetime.datetime.now().time()
print "Finished choosing players to analyze and gathering their features."
print current_time.isoformat()


