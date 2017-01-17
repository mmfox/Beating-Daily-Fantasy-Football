import nflgame
import datetime
import csv
import numpy as np
import random


# Consume and correctly format draft kings salary data
data = np.genfromtxt('DKSalaries.csv',delimiter=',', dtype=str)
salary_data =data[:,:3]
for j in range(0, len(salary_data)):
    salary_data[j][0] = salary_data[j][0][1:len(salary_data[j][0])-1]
    if(salary_data[j][0] != 'DST'):
        first_char = salary_data[j][1][1]
        for i in range(0, len(salary_data[j][1])):
            if (salary_data[j][1][i] == ' '):
                new_name = first_char + '.' + salary_data[j][1][i+1:len(salary_data[j][1])-1]
        salary_data[j][1] = new_name
    else: 
        salary_data[j][1] = salary_data[j][1][1:len(salary_data[j][1])-1]

final_wr_data = np.genfromtxt('wr_final_data.csv',delimiter=',', dtype=str)
final_qb_data = np.genfromtxt('qb_final_data.csv',delimiter=',', dtype=str)
final_rb_data = np.genfromtxt('rb_final_data.csv',delimiter=',', dtype=str)

wr_theta = np.genfromtxt('wr_theta.csv',delimiter=',')
qb_theta = np.genfromtxt('qb_theta.csv',delimiter=',')
rb_theta = np.genfromtxt('rb_theta.csv',delimiter=',')

temp_master_wr_array = []
for i in range(0, len(final_wr_data)):
    temp_master_wr_array.append(['', 'NONE', 0, 0, 0])
    temp_master_wr_array[i][0] = final_wr_data[i][0]
    for j in range(0, len(salary_data)):
       if(salary_data[j][1] == final_wr_data[i][0]):
           temp_master_wr_array[i][1] = salary_data[j][0]
           temp_master_wr_array[i][2] = salary_data[j][2]
           break
    proj_pts = 0
    for k in range(0,len(wr_theta)-1):
        proj_pts += wr_theta[k] * float(final_wr_data[i][k+1])
    temp_master_wr_array[i][3] = proj_pts
    temp_master_wr_array[i][4] = final_wr_data[i][len(final_wr_data[i])-1]


temp_master_rb_array = []
for i in range(0, len(final_rb_data)):
    temp_master_rb_array.append(['', 'NONE', 0, 0, 0])
    temp_master_rb_array[i][0] = final_rb_data[i][0]
    for j in range(0, len(salary_data)):
       if(salary_data[j][1] == final_rb_data[i][0]):
           temp_master_rb_array[i][1] = salary_data[j][0]
           temp_master_rb_array[i][2] = salary_data[j][2]
           break
    proj_pts = 0
    for k in range(0,len(rb_theta)-1):
        proj_pts += rb_theta[k] * float(final_rb_data[i][k+1])
    temp_master_rb_array[i][3] = proj_pts
    temp_master_rb_array[i][4] = final_rb_data[i][len(final_rb_data[i])-1]

master_rb_array = []
for i in range(0, len(temp_master_rb_array)):
    if(temp_master_rb_array[i][1] == 'RB'):
        master_rb_array.append(temp_master_rb_array[i])

temp_master_qb_array = []
for i in range(0, len(final_qb_data)):
    temp_master_qb_array.append(['', 'NONE', 0, 0, 0])
    temp_master_qb_array[i][0] = final_qb_data[i][0]
    for j in range(0, len(salary_data)):
       if(salary_data[j][1] == final_qb_data[i][0]):
           temp_master_qb_array[i][1] = salary_data[j][0]
           temp_master_qb_array[i][2] = salary_data[j][2]
           break
    proj_pts = 0
    for k in range(0,len(qb_theta)-1):
        proj_pts += qb_theta[k] * float(final_qb_data[i][k+1])
    temp_master_qb_array[i][3] = proj_pts
    temp_master_qb_array[i][4] = final_qb_data[i][len(final_qb_data[i])-1]

master_qb_array = []
for i in range(0, len(temp_master_qb_array)):
    if(temp_master_qb_array[i][1] == 'QB'):
        master_qb_array.append(temp_master_qb_array[i])


# Now let's split the wr_array into WRs and TEs
master_wr_array = []
master_te_array = []
for i in range(0, len(temp_master_wr_array)):
    if(temp_master_wr_array[i][1] == 'WR'):
        master_wr_array.append(temp_master_wr_array[i])
    elif(temp_master_wr_array[i][1] == 'TE'):
        master_te_array.append(temp_master_wr_array[i])

master_flex_array = master_rb_array + master_wr_array + master_te_array

# Manually input DST info
master_dst_array = []
master_dst_array.append(['Falcons', 3900, 10, 26])
master_dst_array.append(['Texans', 3800, 10, 8])
master_dst_array.append(['Bills', 3700, 10, 6])
master_dst_array.append(['Broncos', 3600, 10, 6])
master_dst_array.append(['Vikings', 3500, 10, 7])
master_dst_array.append(['Chiefs', 3400, 10, 11])
master_dst_array.append(['Packers', 3200, 10, 19])
master_dst_array.append(['Ravens', 3100, 10, 15])
master_dst_array.append(['Cardinals', 3000, 10, 7])
master_dst_array.append(['Eagles', 2900, 10, 10])
master_dst_array.append(['Giants', 2900, 10, 13])
master_dst_array.append(['Patriots', 2800, 10, 12])
master_dst_array.append(['Bengals', 2800, 10, 9])
master_dst_array.append(['Steelers', 2800, 10, 8])
master_dst_array.append(['Cowboys', 2700, 10, 13])
master_dst_array.append(['Titans', 2700, 10, 11])
master_dst_array.append(['Raiders', 2700, 10, 7])
master_dst_array.append(['Chargers', 2700, 10, 4])
master_dst_array.append(['Jaguars', 2600, 10, 2])
master_dst_array.append(['Lions', 2600, 10, 5])
master_dst_array.append(['Buccaneers', 2500, 10, 11])
master_dst_array.append(['Colts', 2500, 10, 4])
master_dst_array.append(['Bears', 2400, 10, 14])
master_dst_array.append(['Saints', 2400, 10, 5])
master_dst_array.append(['49ers', 2300, 10, 8])
master_dst_array.append(['Browns', 2200, 10, 4])

iterations = 1000000
money_made = 0
money_risked = 0
max_score = 0

print "WR/TE/RB/QB/FLEX/DST"
print len(master_wr_array)
print len(master_te_array)
print len(master_rb_array)
print len(master_qb_array)
print len(master_flex_array)
print len(master_dst_array)

while(1):
   max_score = 1
for i in range(0, iterations):
    wrs  = random.sample(master_wr_array, 3)
    te   = random.sample(master_te_array, 1)
    rbs  = random.sample(master_rb_array, 2)
    qb   = random.sample(master_qb_array, 1)
    flex = random.sample(master_flex_array, 1)
    dst  = random.sample(master_dst_array, 1)

    flexList = []
    flexList.append(wrs[0][0])
    flexList.append(wrs[1][0])
    flexList.append(wrs[2][0])
    flexList.append(rbs[0][0])
    flexList.append(rbs[1][0])
    flexList.append(te[0][0])
    while(flex[0][0] in flexList):
        flex = random.sample(master_flex_array, 1)

    cost = int(wrs[0][2]) + int(wrs[1][2]) + int(wrs[2][2]) + int(te[0][2]) + int(rbs[0][2]) + int(rbs[1][2]) + int(qb[0][2]) + int(flex[0][2]) + dst[0][1]
    proj_pts = float(wrs[0][3]) + float(wrs[1][3]) + float(wrs[2][3]) + float(te[0][3]) + float(rbs[0][3]) + float(rbs[1][3]) + float(qb[0][3]) + float(flex[0][3]) + dst[0][2]
    actual_pts = float(wrs[0][4]) + float(wrs[1][4]) + float(wrs[2][4]) + float(te[0][4]) + float(rbs[0][4]) + float(rbs[1][4]) + float(qb[0][4]) + float(flex[0][4]) + dst[0][3]
    #print "Proj_pts " + repr(proj_pts)
    #print "Actual_pts " + repr(actual_pts)
    if(cost < 50000 and proj_pts > 70):
        money_risked += 3
        print "Proj_pts " + repr(proj_pts)
        print "Actual_pts " + repr(actual_pts)
        if(actual_pts > max_score):
            max_score = actual_pts
            max_wrs = wrs
            max_te = te
            max_rbs = rbs
            max_flex = flex
            max_qb = qb
            max_dst = dst
        if(actual_pts < 134.6):
            money_made -= 3
        elif(actual_pts < 144.78):
            money_made += 2
        elif(actual_pts < 154.04):
            money_made += 3
        elif(actual_pts < 162.18):
            money_made += 4
        elif(actual_pts < 168.2):
            money_made += 5
        elif(actual_pts < 173.04):
            money_made += 6
        elif(actual_pts < 177.4):
            money_made += 7
        elif(actual_pts < 182):
            money_made += 9
        elif(actual_pts < 186.92):
            money_made += 12
        elif(actual_pts < 191.66):
            money_made += 17
        elif(actual_pts < 195.24):
            money_made += 22
        elif(actual_pts < 198.16):
            money_made += 27
        elif(actual_pts < 200.84):
            money_made += 32
        elif(actual_pts < 203.54):
            money_made += 37
        elif(actual_pts < 206.96):
            money_made += 47
        elif(actual_pts < 208.54):
            money_made += 57
        elif(actual_pts < 210.14):
            money_made += 72
        elif(actual_pts < 211.44):
            money_made += 97
        elif(actual_pts < 213.22):
            money_made += 147
        elif(actual_pts < 215.66):
            money_made += 197
        elif(actual_pts < 218.42):
            money_made += 297
        elif(actual_pts < 221.16):
            money_made += 397
        elif(actual_pts < 222.14):
            money_made += 497
        elif(actual_pts < 225.72):
            money_made += 747
        elif(actual_pts < 226.26):
            money_made += 997
        elif(actual_pts < 228.36):
            money_made += 1497
        elif(actual_pts < 230.26):
            money_made += 1997
        elif(actual_pts < 234.64):
            money_made += 2997
        elif(actual_pts < 234.96):
            money_made += 4997
        elif(actual_pts < 237.46):
            money_made += 7497
        elif(actual_pts < 237.74):
            money_made += 9997
        elif(actual_pts < 239.36):
            money_made += 14997
        elif(actual_pts < 243.24):
            money_made += 24997
        else:
            money_made += 49997

print "Money made " + repr(money_made)
print "Money risked " + repr(money_risked)
print "Max Score " + repr(max_score)
print "Max WRs " + max_wrs[0][0] + ' & ' + max_wrs[1][0] + ' & ' + max_wrs[2][0]
print "Max TE " + max_te[0][0]
print "Max RBs " + max_rbs[0][0] + ' & ' + max_rbs[1][0]
print "Max Flex " + max_flex[0][0]
print "Max QB " + max_qb[0][0]
print "Max DST " + max_dst[0][0]



   



