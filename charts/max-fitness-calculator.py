
# distance from nest to food (m)
gap_40_100 = 0.6
gap_40_120 = 0.8
gap_50_100 = 0.5
gap_50_120 = 0.7
gap_60_100 = 0.4
gap_60_120 = 0.6

# from kilobots experiments
turn180 = 72
forwards1m = 160
totalSteps = 800

# first configuration
gap = gap_60_100
journey = forwards1m * gap + 1
firstTrip = journey * 2 + turn180
otherTrips = journey * 2 + turn180 * 2

count = 0
check = firstTrip
max_fitness1 = 1.0
while check < totalSteps and count < 10:
    check += otherTrips
    if check < totalSteps:
        max_fitness1 += 1.0
    else:
        max_fitness1 += (otherTrips - (check - totalSteps)) / otherTrips
    count += 1
print(max_fitness1)

# second configuration
gap = gap_60_120
journey = forwards1m * gap + 1
firstTrip = journey * 2 + turn180
otherTrips = journey * 2 + turn180 * 2

count = 0
check = firstTrip
max_fitness2 = 1.0
while check < totalSteps and count < 10:
    check += otherTrips
    if check < totalSteps:
        max_fitness2 += 1.0
    else:
        max_fitness2 += (otherTrips - (check - totalSteps)) / otherTrips
    count += 1
print(max_fitness2)

# averaged maximum fitness
max_fitness = (max_fitness1 + max_fitness2) / 2
print(max_fitness)
