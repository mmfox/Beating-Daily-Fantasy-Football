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
    points.append(getFantasyPoints(yr, wk-1, pid))
    points.append(getFantasyPoints(yr, wk-2, pid))
    points.append(getFantasyPoints(yr, wk-3, pid))
    points.append(getFantasyPoints(yr, wk-4, pid))
    points.append(getFantasyPoints(yr, wk-5, pid))
    points.append(getFantasyPoints(yr, wk-6, pid))
    for i in range(0,6):
       if(points[i] == 0):
           leave_out_week = i
           break 
    added = 0
    games3 = []
    games5 = []
    points3 = 0
    points5 = 0
    for i in range(0,6):
        if(i != leave_out_week):
            if(added < 1):
               games1 = games[i]
               points1 = points[i];
            if(added < 3):
               games3 = games3 + games[i]
               points3 = points3 + points[i]
            if(added < 5):
               games5 = games5 + games[i]
               points5 = points5 + points[i]
            added = added + 1
    play1 = nflgame.combine_game_stats(games1)
    play3 = nflgame.combine_game_stats(games3)
    play5 = nflgame.combine_game_stats(games5)
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
    local_wr_data = [p1.name, p1.receiving_yds, p1.receiving_tds, p1.receiving_rec, p3.receiving_yds, p3.receiving_tds, p3.receiving_rec, p5.receiving_yds, p5.receiving_tds, p5.receiving_rec]
    actual_points = getFantasyPoints(yr, wk, pid)
    local_wr_data.append(actual_points)
    print p1.name 
    print actual_points
    WR_DATA.append(local_wr_data)


def populate_qb_data(yr, wk, p1, p3, p5, points1, points3, points5, pid):
    global QB_DATA
    local_qb_data = [p1.name, p1.passing_yds, p1.passing_tds, p1.passing_att, p1.passing_cmp, p1.passing_ints, p3.passing_yds, p3.passing_tds, p3.passing_att, p3.passing_cmp, p3.passing_ints, p5.passing_yds, p5.passing_tds, p5.passing_att, p5.passing_cmp, p5.passing_ints]
    actual_points = getFantasyPoints(yr, wk, pid)
    local_qb_data.append(actual_points)
    print p1.name 
    print actual_points
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

    local_rb_data = [p1.name, p1.rushing_yds, p1.rushing_tds, p1.rushing_att, p1.receiving_yds, p1.receiving_tds, p1.receiving_rec, p3.rushing_yds, p3.rushing_tds, p3.rushing_att, p3.receiving_yds, p3.receiving_tds, p3.receiving_rec, p5.rushing_yds, p5.rushing_tds, p5.rushing_att, p5.receiving_yds, p5.receiving_tds, p5.receiving_rec]
    actual_points = getFantasyPoints(yr, wk, pid)
    print p1.name 
    print actual_points
    local_rb_data.append(actual_points)
    RB_DATA.append(local_rb_data)


def getFantasyPoints(yr, wk, pid):
    points = 0
    g = nflgame.games(yr, week=wk)
    play = nflgame.combine_game_stats(g)
    (player_exists, p) = findPlayerById(play, pid)
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
WR_DATA = []
RB_DATA = []
QB_DATA = []
games = []

for year in range(2016, 2017):
    local_week = 14
    players = []
    games.append(nflgame.games(year, week=local_week-1))
    games.append(nflgame.games(year, week=local_week-2))
    games.append(nflgame.games(year, week=local_week-3))
    games.append(nflgame.games(year, week=local_week-4))
    games.append(nflgame.games(year, week=local_week-5))
    games.append(nflgame.games(year, week=local_week-6))
    combo_3_games = games[0] + games[1] + games[2]
    players.append(nflgame.combine_game_stats(games[0]))
    players.append(nflgame.combine_game_stats(games[1]))
    players_last_3 = nflgame.combine_game_stats(combo_3_games);
    print "Starting WRs"
    for p3 in players_last_3.receiving().sort('receiving_yds').limit(60):
        pid = p3.playerid
        (p1_present, p1) = findPlayerById(players[0], pid)
        if(p1_present == 0):
            (p1_present, p1) = findPlayerById(players[1], pid)
        if(p1_present):
            populate_data(year, local_week, pid, 0)
    print "Starting QBs"
    for p3 in players_last_3.passing().sort('passing_yds').limit(25):
        pid = p3.playerid
        (p1_present, p1) = findPlayerById(players[0], pid)
        if(p1_present == 0):
            (p1_present, p1) = findPlayerById(players[1], pid)
        if(p1_present):
            populate_data(year, local_week, pid, 2)
    print "Starting RBs"
    for p3 in players_last_3.rushing().sort('rushing_yds').limit(25):
        pid = p3.playerid
        (p1_present, p1) = findPlayerById(players[0], pid)
        if(p1_present == 0):
            (p1_present, p1) = findPlayerById(players[1], pid)
        if(p1_present):
            populate_data(year, local_week, pid, 1)

print "Writing out data"
with open('wr_final_data.csv', 'wb') as wr_csvfile:
    wr_writer = csv.writer(wr_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(WR_DATA)):
        wr_writer.writerow(WR_DATA[i])

with open('rb_final_data.csv', 'wb') as rb_csvfile:
    rb_writer = csv.writer(rb_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(RB_DATA)):
        rb_writer.writerow(RB_DATA[i])

with open('qb_final_data.csv', 'wb') as qb_csvfile:
    qb_writer = csv.writer(qb_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(QB_DATA)):
        qb_writer.writerow(QB_DATA[i])


current_time = datetime.datetime.now().time()
print "Finished choosing players to analyze and gathering their features."
print current_time.isoformat()


