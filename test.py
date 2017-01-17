import nflgame
import datetime
import csv

def findPlayerById(player_list, pid):
    for p in player_list:
        lastp = p
        if(p.playerid == pid):
            return (1, p)
    return (0, lastp)

def populate_wr_data(yr, wk, p1, p3, p5, pid):
    global WR_DATA
    local_wr_data = [p1.receiving_yds, p1.receiving_tds, p1.receiving_rec, p3.receiving_yds, p3.receiving_tds, p3.receiving_rec, p5.receiving_yds, p5.receiving_tds, p5.receiving_rec]
    print local_wr_data
    actual_points = getFantasyPoints(yr, wk, pid)
    print actual_points
    local_wr_data.append(actual_points)
    WR_DATA.append(local_wr_data)

def populate_qb_data(yr, wk, p1, p3, p5, pid):
    global QB_DATA
    local_qb_data = [p1.passing_yds, p1.passing_tds, p1.passing_att, p1.passing_cmp, p1.passing_ints, p3.passing_yds, p3.passing_tds, p3.passing_att, p3.passing_cmp, p3.passing_ints, p5.passing_yds, p5.passing_tds, p5.passing_att, p5.passing_cmp, p5.passing_ints]
    print local_qb_data
    actual_points = getFantasyPoints(yr, wk, pid)
    print actual_points
    local_qb_data.append(actual_points)
    QB_DATA.append(local_qb_data)

def populate_rb_data(yr, wk, p1, p3, p5, pid):
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

    local_rb_data = [p1.rushing_yds, p1.rushing_tds, p1.rushing_att, p1.receiving_yds, p1.receiving_tds, p1.receiving_rec, p3.rushing_yds, p3.rushing_tds, p3.rushing_att, p3.receiving_yds, p3.receiving_tds, p3.receiving_rec, p5.rushing_yds, p5.rushing_tds, p5.rushing_att, p5.receiving_yds, p5.receiving_tds, p5.receiving_rec]
    print local_rb_data
    actual_points = getFantasyPoints(yr, wk, pid)
    print actual_points
    local_rb_data.append(actual_points)
    RB_DATA.append(local_rb_data)

def getFantasyPoints(yr, wk, pid):
    points = 0
    games = nflgame.games(yr, week=wk)
    players = nflgame.combine_game_stats(games)
    (player_exists, p) = findPlayerById(players, pid)
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
#
#current_time = datetime.datetime.now().time()
#print "Time Started \n"
#print current_time.isoformat()
#print "\n"
#
#WR_DATA = []
#RB_DATA = []
#QB_DATA = []
#
#for year in range(2009, 2016):
#    for local_week in range(6, 17):
#        games = []
#        games.append(nflgame.games(year, week=local_week-5))
#        games.append(nflgame.games(year, week=local_week-4))
#        games.append(nflgame.games(year, week=local_week-3))
#        games.append(nflgame.games(year, week=local_week-2))
#        games.append(nflgame.games(year, week=local_week-1))
#        combo_games = games[4]
#        combo_3_games = games[4] + games[3] + games[2]
#        combo_5_games = combo_3_games + games[1] + games[0]
#        players1 = nflgame.combine_game_stats(combo_games)
#        players3 = nflgame.combine_game_stats(combo_3_games)
#        players5 = nflgame.combine_game_stats(combo_5_games)
#        for p3 in players3.receiving().sort('receiving_yds').limit(60):
#            pid = p3.playerid
#            (p1_present, p1) = findPlayerById(players1, pid)
#            if(p1_present):
#                (p5_present, p5) = findPlayerById(players5, pid)
#                populate_wr_data(year, local_week, p1, p3, p5, pid)
#        for p3 in players3.passing().sort('passing_yds').limit(25):
#            pid = p3.playerid
#            (p1_present, p1) = findPlayerById(players1, pid)
#            if(p1_present):
#                (p5_present, p5) = findPlayerById(players5, pid)
#                populate_qb_data(year, local_week, p1, p3, p5, pid)
#        for p3 in players3.rushing().sort('rushing_yds').limit(25):
#            pid = p3.playerid
#            (p1_present, p1) = findPlayerById(players1, pid)
#            if(p1_present):
#                (p5_present, p5) = findPlayerById(players5, pid)
#                populate_rb_data(year, local_week, p1, p3, p5, pid)
#
#
#with open('wr_data.csv', 'wb') as wr_csvfile:
#    wr_writer = csv.writer(wr_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for i in range(0, len(WR_DATA)):
#        wr_writer.writerow(WR_DATA[i])
#
#with open('rb_data.csv', 'wb') as rb_csvfile:
#    rb_writer = csv.writer(rb_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for i in range(0, len(RB_DATA)):
#        rb_writer.writerow(RB_DATA[i])
#
#with open('qb_data.csv', 'wb') as qb_csvfile:
#    qb_writer = csv.writer(qb_csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for i in range(0, len(QB_DATA)):
#        qb_writer.writerow(QB_DATA[i])
#
#
#current_time = datetime.datetime.now().time()
#print "Finished choosing players to analyze and gathering their features."
#print current_time.isoformat()

WR_DATA = []
RB_DATA = []
QB_DATA = []

for year in range(2016, 2017):
    for local_week in range(6, 10):
        print "Year, Week"
        print year
        print local_week
        games = []
        games.append(nflgame.games(year, week=local_week-5))
        games.append(nflgame.games(year, week=local_week-4))
        games.append(nflgame.games(year, week=local_week-3))
        games.append(nflgame.games(year, week=local_week-2))
        games.append(nflgame.games(year, week=local_week-1))
        combo_games = games[4]
        combo_3_games = games[4] + games[3] + games[2]
        combo_5_games = combo_3_games + games[1] + games[0]
        players1 = nflgame.combine_game_stats(combo_games)
        players3 = nflgame.combine_game_stats(combo_3_games)
        players5 = nflgame.combine_game_stats(combo_5_games)
        for p3 in players3.receiving().sort('receiving_yds').limit(2):
            print "WR"
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players1, pid)
            if(p1_present):
                (p5_present, p5) = findPlayerById(players5, pid)
                print p5.name
                populate_wr_data(year, local_week, p1, p3, p5, pid)
        for p3 in players3.passing().sort('passing_yds').limit(2):
            print "QB"
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players1, pid)
            if(p1_present):
                (p5_present, p5) = findPlayerById(players5, pid)
                print p5.name
                populate_qb_data(year, local_week, p1, p3, p5, pid)
        for p3 in players3.rushing().sort('rushing_yds').limit(2):
            print "RB"
            pid = p3.playerid
            (p1_present, p1) = findPlayerById(players1, pid)
            if(p1_present):
                (p5_present, p5) = findPlayerById(players5, pid)
                print p5.name
                populate_rb_data(year, local_week, p1, p3, p5, pid)

