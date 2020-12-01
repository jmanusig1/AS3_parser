import csv
import json 

#list of the important data points per player
compiled_data = []

#list of players (full data)
players = []

#list of players (sorted by time)
sorted_players = []

#open csv
with open('b.csv') as file: 
    b_file = csv.reader(file)

    #variables to keep track of time
    start_time = 0
    end_time = 0
    elapsed_time = 0

    #variable to keep track of the number of clicks
    num_clicks = 0

    #variable to keep track of the players
    player = []

    #sort the csv by UID
    sorted_csv = sorted(b_file, key=lambda  row: row[1])

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

        prev_seed = ""

        num_clicks = 0

        for row in p:

            num_clicks += 1 

            if('seed' in row[5] and 'elapsed' in row[5]):
                
                data = json.loads(row[5])

                compiled_data.append([row[1], data["elapsed"], num_clicks])

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
        average_clicks += entry[2]
        count += 1

    return (average_clicks / count)

def get_average_per_player(data_array):

    averages = []
    caverage = 0
    taverage = 0
    count = 0

    uid = []
    prev_uid = ""

    for entry in data_array:

        if(len(uid) == 0 ):
            uid.append(entry[0])
            taverage += entry[1]
            caverage += entry[2]
            count += 1
            prev_uid = entry
        elif(entry[0] not in uid):
            averages.append([prev_uid, float(taverage/count), float(caverage/count), count])
            uid.append(entry[0])
            count = 0
            taverage = 0
            caverage = 0
            taverage += entry[1]
            caverage += entry[2]
            count += 1
            prev_uid = entry[0]
        else:
            taverage += entry[1]
            caverage += entry[2]
            count += 1

    return averages

print("average time: " + str(get_average_time(compiled_data)))
print("average clicks: " + str(get_average_clicks(compiled_data)))

p_avg = get_average_per_player(compiled_data)

for p in p_avg:
    print(p)

fields = ['UID', 'Avg Times', 'Avg Clicks', 'Count']

b_data_csv = 'b_data.csv'

with open(b_data_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(fields)

    csvwriter.writerows(p_avg)
