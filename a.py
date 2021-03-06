import csv

#list of victory times per puzzle
victory_times = []

#list of mouse clicks per puzzle
clicks = []

#list of players (full data)
players = []

#list of players (sorted by time)
sorted_players = []

#open csv
with open('a.csv') as file: 
    a_file = csv.reader(file)

    #variables to keep track of time
    start_time = 0
    end_time = 0
    elapsed_time = 0

    #variable to keep track of the number of clicks
    num_clicks = 0

    #variable to keep track of the players
    player = []

    #sort the csv by UID
    sorted_csv = sorted(a_file, key=lambda  row: row[1])

    #then place all the players into an array that contains all their moves
    for entry in sorted_csv:
        
        if(entry[0] == "Timestamp"):
            continue

        #if player is empty, then we just add the player
        if(len(player) == 0):
            player.append(entry)
        
        #if we encounter a new player, push to the players array and reset 
        elif entry[1] not in player[0][1]:
            
            players.append(player)
            player = []
            player.append(entry)
        
        #otherwise keep populating the player array
        else:
            player.append(entry)

    #then sort the player moves by time
    for entry in players:
        sorted_player = sorted(entry, key=lambda  row: row[2])
        sorted_players.append(sorted_player) 

    #go through the fully sorted csv (by plater + time)
    for p in players:
    
        #player base of UID's
        uid = []
        
        for row in p:
            
            #skip the first row
            if row[0] == 'Timestamp':
                continue

            #first find unique user
            if row[1] not in uid:
                uid.append(row[1])
                
                num_clicks = 0

                start_time = row[2]


            if(row[3] == 'mousedown'):
                num_clicks += 1

            #check when we get a victory
            if row[3] == 'victory':
                
                #if so, set the end time
                end_time = row[2]

                #calculate the time elapsed
                elapsed_time = (int(end_time) - int(start_time))


                #and append the the list of times
                victory_times.append([row[1], elapsed_time])
                clicks.append ([row[1], num_clicks])

                #then reset the start time
                start_time = row[2]
                num_clicks = 0

def get_average_time(times_array):
    average_time = 0
    count = 0

    for entry in times_array:
        average_time += entry[1]
        count += 1

    return (average_time / count)

def get_average_clicks(clicks_array):
    average_clicks = 0
    count = 0

    for entry in clicks_array:
        average_clicks += entry[1]
        count += 1

    return (average_clicks / count)

def get_average_per_player(data_array):

    averages = []
    average = 0
    count = 0

    uid = []
    prev_uid = ""

    for entry in data_array:

        if(len(uid) == 0 ):
            uid.append(entry[0])
            average += entry[1]
            count += 1
            prev_uid = entry
        elif(entry[0] not in uid):
            
            averages.append([prev_uid, float(average/count), count])

            uid.append(entry[0])
            count = 0
            average = 0
            average += entry[1]
            count += 1
            prev_uid = entry[0]
        else:
            average += entry[1]
            count += 1

    return averages

#print(victory_times)

print("average time: " + str(get_average_time(victory_times)))
print("average clicks: " + str(get_average_clicks(clicks)))

player_avg_clicks = get_average_per_player(clicks)
player_avg_times = get_average_per_player(victory_times)

fields1 = ['UID', 'Avg Clicks', 'Count']
fields2 = ['UID', 'Avg Times', 'Count']

a_clicks_csv = 'a_clicks.csv'
a_times_csv = 'a_times.csv'

with open(a_clicks_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(fields1)

    csvwriter.writerows(player_avg_clicks)

with open(a_times_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(fields2)

    csvwriter.writerows(player_avg_times)