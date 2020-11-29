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

        #if player is empty, then we just add the player
        if(len(player) == 0):
            player.append(entry)
        
        #if we encounter a new player, push to the players array and reset 
        elif entry[1] not in player:
            
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
    for p in sorted_players:

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
        if(entry[1] > 10000):
            print(entry)
        average_clicks += entry[1]
        count += 1

    return (average_clicks / count)

def get_average_clicks_per_player(clicks_array):

    averages = []
    average_clicks = 0
    count = 0

    uid = []
    prev_uid = ""

    for entry in clicks_array:

        if(len(uid) == 0 ):
            uid.append(entry[0])
            average_clicks += entry[1]
            count += 1
            prev_uid = entry
        elif(entry[0] not in uid):
            uid.append(entry[0])



            count = 0
            average_clicks = 0
            average_clicks += entry[1]
            count += 1
        else:
            average_clicks += entry[1]
            count += 1

print("average time: " + str(get_average_time(victory_times)))
print("average clicks: " + str(get_average_clicks(clicks)))

#player_avg = get_average_clicks_per_player(clicks)

for entry in player_avg:
    print(entry)