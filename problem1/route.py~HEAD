'''
Created on Sep 16, 2016

@author: Rohil
'''
#Question 1) ASTAR works best for calculating the least distance, least time and the scenic route between two cities. 
# IDS works best for calculating the path having least number of segments. 

#Question 2) For my program IDS seems to be working best for all the routing options. I used a loop for 1000 iterations and the time
# taken by BFS was 98.78 seconds, DFS took 170.15 seconds, ASTAR took 95.52 seconds and IDS took 89.72 seconds.

#Question 3) According to my observations, ASTAR uses the least amount of memory. The maximum length of fringe for ASTAR was 5,
# whereas for BFS was 18, DFS was 495 and IDS was also 18. Hence, ASTAR uses the least amount of memory by almost a factor of 3

#Question 4) I used the EUCLIDEAN distance to calculate the heuristic. Euclidean distance between the successor and the start city
# and between the successor and the goal city will tell my program how far is it from the goal. It is a pretty good heuristic because it
# calculates the straight line distance between two nodes and hence that is the shortest path and therefore it underestimates the 
# the result and hence is admissible. We can make it better if we have better knowledge about the geography of the map and how the roads
# are laid out. If we have the information about the turns and a geographical road map, I think we can modify our heuristic to work better
# and hence it can give a more optimal and quick result.

#Question 5) Blanc-Sablon,_Quebec is the farthest city from Bloomington,_Indiana with the shortest distance of
# 7315 miles


# While calling ASTAR search for segments, it is better to call the IDS method because it will return
# the goal at the lowest level i.e. having least segments.


import sys

# ----READING THE COMMAND LINE ARGUMENTS----

def readingFromCommandLine():
    if(len(sys.argv) < 5):
        return
    start_city = sys.argv[1]
    end_city = sys.argv[2]
    routing_option = sys.argv[3]
    routing_algorithm = sys.argv[4]
    return [start_city,end_city, routing_option, routing_algorithm]

def readFromFile():
    list_1 = []
    with open("road-segments.txt", "r") as roadFile:
        for line in roadFile:
            list_1.append(line.split(" "))
    return list_1

# ----CREATE A DICTIONARY OF THE ROAD-SEGMENTS----

def creatingADictionary():
    list_1 = readFromFile()
    dictionary = {}
    for i in range(0,len(list_1)):
        if list_1[i][0] in dictionary.keys():
            dictionary[list_1[i][0]].append([list_1[i][1]+" "+list_1[i][2]+" "+list_1[i][3]+" "+list_1[i][4]])
        else:
            dictionary[list_1[i][0]] = [[list_1[i][1]+" "+list_1[i][2]+" "+list_1[i][3]+" "+list_1[i][4]]]
            
        if list_1[i][1] in dictionary.keys():
            dictionary[list_1[i][1]].append([list_1[i][0]+" "+list_1[i][2]+" "+list_1[i][3]+" "+list_1[i][4]])
        else:
            dictionary[list_1[i][1]] = [[list_1[i][0]+" "+list_1[i][2]+" "+list_1[i][3]+" "+list_1[i][4]]]
    return dictionary

# ----ERROR CHECKING OF COMMAND LINE ARGUMENTS----

def readFromGPSFile():
    cities = readingFromCommandLine()
    citiesList = []
    with open("city-gps.txt","r") as gpsFile:
        for line in gpsFile:
            cityName = line.split(" ")
            citiesList.append(cityName[0])
    if(cities[0] not in citiesList):
        print("Please enter a valid start city! Exiting.\n")
        sys.exit()
    if(cities[1] not in citiesList):
        print("Please enter a valid end city! Exiting.\n")
        sys.exit()
        
# ----CALCULATE THE SUCCESSORS----

def successors(nextNode):
    inside = "".join(nextNode).split(" ")
    if(not (dictionary.get(inside[0]))):
        return [None]
    return [dictionary[inside[0]][i] for i in range(0,len(dictionary[inside[0]]))]

# ----CHECK IF THE GOAL HAS BEEN REACHED----

def is_goal(node, endCity):
    if(node == endCity):
        return True
    return False

# Distance for Breadth First Search
# Initial state: [startCity, endCity]
# Successor Function = Pop the node(road segment) at the front i.e implement the fringe as a queue until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal State = A path from startCity to endCity
# Cost = Each of the path is associated with the distance between the two nodes
# We hope to find the path with the least distance, if the code finds two paths having different
# distances, then we will select the path with the least distance                    
def breadthFirstSearchForDistance(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
    
    while(len(fringe) > 0):
        initialVal = "".join(fringe[0])
        for s in successors(fringe.pop(0)):
            if(s != None):
                cityName = "".join(s).split(" ")
                successorValue = "".join(s)
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    visitedCities.append(cityName[0])
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        goalDictionary = [goalPath]
                        return goalDictionary
                        break
                    fringe.append(s)
                elif(cityName[0] != startCity):
                    stringSplit = "".join(s).split(" ")
                    successorValue = "".join(s)
                    newPath = randomList[initialVal] + s
                    if stringSplit[0] in str(randomList.keys()):
                        for val in randomList.keys():
                            if(stringSplit[0] in str(val)):
                                oldPath = randomList[val]
                    distOld = calcDis(oldPath)
                    distNew = calcDis(newPath)
                    if(distOld > distNew):
                        randomList[successorValue] = newPath
                        
# Time for Breadth First Search
# Distance for Breadth First Search
# Initial state: [startCity, endCity]
# Successor Function = Pop the node(road segment) at the front i.e implement the fringe as a queue until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal State = A path from startCity to endCity
# Cost = Each of the path is associated with the time to travel between the two nodes
# We hope to find the path with the least time to travel, if the code finds two paths having different
# travelling times, then we will select the path with the least time                      
def breadthFirstSearchForTime(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
            
    while(len(fringe) > 0):
        initialVal = "".join(fringe[0])
        for s in successors(fringe.pop(0)):
            if(s != None):
                cityName = "".join(s).split(" ")
                successorValue = "".join(s)
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    visitedCities.append(cityName[0])
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        goalDictionary = [goalPath]
                        return goalDictionary
                        break
                    fringe.append(s)
                elif(cityName[0] != startCity):
                    stringSplit = "".join(s).split(" ")
                    successorValue = "".join(s)
                    newPath = randomList[initialVal] + s
                    if stringSplit[0] in str(randomList.keys()):
                        for val in randomList.keys():
                            if(stringSplit[0] in str(val)):
                                oldPath = randomList[val]
                    timeOld = calTime(oldPath)
                    timeNew = calTime(newPath)
                    if(timeOld > timeNew):
                        randomList[successorValue] = newPath
                        
# Breadth first search for Segments  
# Initial state: [startCity, endCity]
# Successor Function = Pop the node(road segment) at the front i.e implement the fringe as a queue until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal State = A path from startCity to endCity
# Cost = A single road joining two cities is considered as a single segment
# We hope to find the path with the least segments, if the code finds two paths having different
# segments, then we will select the path with the least number of segments i.e it visits least number
# of cities                   
def breadthFirstSearchForSegments(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
            
    while(len(fringe) > 0):
        initialVal = "".join(fringe[0])
        for s in successors(fringe.pop(0)):
            if(s != None):
                cityName = "".join(s).split(" ")
                successorValue = "".join(s)
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    visitedCities.append(cityName[0])
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        goalDictionary = [goalPath]
                        return goalDictionary
                        break
                    fringe.append(s)
                elif(cityName[0] != startCity):
                    stringSplit = "".join(s).split(" ")
                    successorValue = "".join(s)
                    newPath = randomList[initialVal] + s
                    if stringSplit[0] in str(randomList.keys()):
                        for val in randomList.keys():
                            if(stringSplit[0] in str(val)):
                                oldPath = randomList[val]
                    segmentOld = calSegments(oldPath)
                    segmentNew = calSegments(newPath)
                    if(segmentOld > segmentNew):
                        randomList[successorValue] = newPath
                        
# Scenic for Breadth First Search
# Initial state: [startCity, endCity]
# Successor Function = Pop the node(road segment) at the front i.e implement the fringe as a queue until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal State = A path from startCity to endCity
# Cost = Each of the path is associated with the speed between the two nodes
# We hope to find the path with the least amount of distance travelled on highways
# i.e to use the road with the speed less than 55, if the code finds two paths having different
# speeds, then we will select the path with the least speed i.e we will use the total path
# travelling through less amount of highways                      
def breadthFirstSearchForScenic(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
    
    while(len(fringe) > 0):
        initialVal = "".join(fringe[0])
        for s in successors(fringe.pop(0)):
            if(s != None):
                cityName = "".join(s).split(" ")
                successorValue = "".join(s)
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    visitedCities.append(cityName[0])
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        goalDictionary = [goalPath]
                        return goalDictionary
                        break
                    fringe.append(s)
                elif(cityName[0] != startCity):
                    stringSplit = "".join(s).split(" ")
                    successorValue = "".join(s)
                    newPath = randomList[initialVal] + s
                    if stringSplit[0] in str(randomList.keys()):
                        for val in randomList.keys():
                            if(stringSplit[0] in str(val)):
                                oldPath = randomList[val]
                    scenicOld = calScenic(oldPath)
                    scenicNew = calScenic(newPath)
                    if(scenicOld > scenicNew):
                        randomList[successorValue] = newPath                        

# Distance for Depth First Search
# Initial state = [startCity, endCity]
# Successor function = Pop the node(road segment) at the back i.e implement the fringe as a stack until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal state = A path from startCity to endCity
# Cost = Each of the path is associated with the distance between the two nodes
# We hope to find the path with the least distance, if the code finds two paths having different
# distances, then we will select the path with the least distance                   
                 
def depthFirstSearchForDistance(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
            
    while(len(fringe) > 0):
        initialVal = "".join(fringe[len(fringe) - 1])
        for s in successors(fringe.pop()):
            if(s != None):
                cityName = "".join(s).split(" ")
                successorValue = "".join(s)
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    visitedCities.append(cityName[0])
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        goalDictionary = [goalPath]
                        return goalDictionary
                        break
                    fringe.append(s)
                elif(cityName[0] != startCity):
                    stringSplit = "".join(s).split(" ")
                    successorValue = "".join(s)
                    newPath = randomList[initialVal] + s
                    if stringSplit[0] in str(randomList.keys()):
                        for val in randomList.keys():
                            if(stringSplit[0] in str(val)):
                                oldPath = randomList[val]
                    distOld = calcDis(oldPath)
                    distNew = calcDis(newPath)
                    if(distOld > distNew):
                        randomList[successorValue] = newPath
                        
# Time for Depth First Search
# Initial state = [startCity, endCity]
# Successor function = Pop the node(road segment) at the back i.e implement the fringe as a stack until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal state = A path from startCity to endCity
# Cost = Each of the path is associated with the time to travel between the two nodes
# We hope to find the path with the least time to travel, if the code finds two paths having different
# travelling times, then we will select the path with the least time             
def depthFirstSearchForTime(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
            
    while(len(fringe) > 0):
        initialVal = "".join(fringe[len(fringe) - 1])
        for s in successors(fringe.pop()):
            if(s != None):
                cityName = "".join(s).split(" ")
                successorValue = "".join(s)
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    visitedCities.append(cityName[0])
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        goalDictionary = [goalPath]
                        return goalDictionary
                        break
                    fringe.append(s)
                elif(cityName[0] != startCity):
                    stringSplit = "".join(s).split(" ")
                    successorValue = "".join(s)
                    newPath = randomList[initialVal] + s
                    if stringSplit[0] in str(randomList.keys()):
                        for val in randomList.keys():
                            if(stringSplit[0] in str(val)):
                                oldPath = randomList[val]
                    timeOld = calTime(oldPath)
                    timeNew = calTime(newPath)
                    if(timeOld > timeNew):
                        randomList[successorValue] = newPath
                        
# Segments for Depth First Search
# Initial state = [startCity, endCity]
# Successor function = Pop the node(road segment) at the back i.e implement the fringe as a stack until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal state = A path from startCity to endCity
# Cost = A single road joining two cities is considered as a single segment
# We hope to find the path with the least segments, if the code finds two paths having different
# segments, then we will select the path with the least number of segments i.e it visits least number
# of cities                        
def depthFirstSearchForSegments(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
            
    while(len(fringe) > 0):
        initialVal = "".join(fringe[len(fringe) - 1])
        for s in successors(fringe.pop()):
            if(s != None):
                cityName = "".join(s).split(" ")
                successorValue = "".join(s)
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    visitedCities.append(cityName[0])
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        goalDictionary = [goalPath]
                        return goalDictionary
                        break
                    fringe.append(s)
                elif(cityName[0] != startCity):
                    stringSplit = "".join(s).split(" ")
                    successorValue = "".join(s)
                    newPath = randomList[initialVal] + s
                    if stringSplit[0] in str(randomList.keys()):
                        for val in randomList.keys():
                            if(stringSplit[0] in str(val)):
                                oldPath = randomList[val]
                    segmentOld = calSegments(oldPath)
                    segmentNew = calSegments(newPath)
                    if(segmentOld > segmentNew):
                        randomList[successorValue] = newPath
                        
# Scenic for Depth First Search
# Initial state = [startCity, endCity]
# Successor function = Pop the node(road segment) at the back i.e implement the fringe as a stack until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal state = A path from startCity to endCity
# Cost = Each of the path is associated with the speed between the two nodes
# We hope to find the path with the least amount of distance travelled on highways
# i.e to use the road with the speed less than 55, if the code finds two paths having different
# speeds, then we will select the path with the least speed i.e we will use the total path
# travelling through less amount of highways                                               
def depthFirstSearchForScenic(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
            
    while(len(fringe) > 0):
        initialVal = "".join(fringe[len(fringe) - 1])
        for s in successors(fringe.pop()):
            if(s != None):
                cityName = "".join(s).split(" ")
                successorValue = "".join(s)
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    visitedCities.append(cityName[0])
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        goalDictionary = [goalPath]
                        return goalDictionary
                        break
                    fringe.append(s)
                elif(cityName[0] != startCity):
                    stringSplit = "".join(s).split(" ")
                    successorValue = "".join(s)
                    newPath = randomList[initialVal] + s
                    if stringSplit[0] in str(randomList.keys()):
                        for val in randomList.keys():
                            if(stringSplit[0] in str(val)):
                                oldPath = randomList[val]
                    scenicOld = calScenic(oldPath)
                    scenicNew = calScenic(newPath)
                    if(scenicOld > scenicNew):
                        randomList[successorValue] = newPath

# ----A STAR SEARCH----
# Initial State = [startCity, endCity]
# Successor Function
# Heuristic Function = Euclidean distance between the startCity and the successor and then between the successor and
# the goal state
# Final state = Path with shortest distance between the startCity and the endCity

# If a city A has a successor B which cannot be found in the city-gps file, then we try to find the successors of city B
# and then calculate the heuristic. Therefore, we assume that that city B does not exist even and therefore a straight road exists
# between city A and city C(successor of city B) 

def astarSearchForDistance(cities):
    startCity = cities[0]
    endCity = cities[1]
    list_1 = []
    fringe = {0:startCity}
    visitedCities = [startCity]
    goalDictionary = []
    randomList = {}
    with open("city-gps.txt","r") as gpsFile:
        for line in gpsFile:
            list_1.append(line.split(" "))
    gpsDictionary = {}
    for i in range(0, len(list_1)):
        gpsDictionary[list_1[i][0]] = list_1[i][1] +" "+ list_1[i][2]
    if(gpsDictionary.get(endCity) != None):
        endCityLocation = gpsDictionary.get(endCity).split(" ")
        endCityLatitude = endCityLocation[0]
        endCityLongitude = endCityLocation[1]
    
    if(gpsDictionary.get(startCity) != None):
        startCityLocation = gpsDictionary.get(startCity).split(" ")
        startCityLatitude = startCityLocation[0]
        startCityLongitude = startCityLocation[1]
    
    while(len(fringe) > 0):
        initialVal = "".join(fringe[min(fringe)])
        for s in successors(popWithLeastValue(fringe)):
            citySplit = "".join(s).split(" ")
            if(gpsDictionary.get(citySplit[0]) != None and citySplit[0] not in visitedCities):
                locationValues = gpsDictionary.get(citySplit[0]).split(" ")
                latitudeVal = locationValues[0]
                longitudeVal = locationValues[1]
                distanceBetweenSuccAndStartCity = calculateEuclideanDistance(startCityLatitude,
                                                startCityLongitude, latitudeVal, longitudeVal)
                distanceBetweenSuccAndGoal = calculateEuclideanDistance(latitudeVal, longitudeVal,
                                                 endCityLatitude, endCityLongitude)
                totalHeuristic = round(distanceBetweenSuccAndStartCity+distanceBetweenSuccAndGoal,4)
                successorValue = "".join(s)
                if(randomList.get(initialVal) != None):
                    value = randomList[initialVal]
                    randomList[successorValue] = value + s
                else:
                    randomList[successorValue] = [initialVal] + s
                if is_goal(citySplit[0], endCity):
                    goalPath = randomList[initialVal]
                    goalPath = goalPath + s
                    randomList[initialVal] = goalPath
                    if(goalDictionary != None):
                        goalDictionary.append(goalPath)
                        return goalDictionary
                
                if(citySplit[0] not in visitedCities):
                    fringe[totalHeuristic] = s
                visitedCities.append(citySplit[0])
                
            elif(citySplit[0] not in visitedCities):
                for s_new in successors(s):
                    citySplit_new = "".join(s_new).split(" ")
                    if(gpsDictionary.get(citySplit_new[0]) != None):
                        if(citySplit_new[0] not in visitedCities):
                            if(gpsDictionary.get(citySplit_new[0]) != None):
                                locationValues = gpsDictionary.get(citySplit_new[0]).split(" ")
                            latitudeVal = locationValues[0]
                            longitudeVal = locationValues[1]
                            distanceBetweenSuccAndStartCity = calculateEuclideanDistance(startCityLatitude,
                                                startCityLongitude, latitudeVal, longitudeVal)
                            distanceBetweenSuccAndGoal = calculateEuclideanDistance(latitudeVal, longitudeVal,
                                                 endCityLatitude, endCityLongitude)
                            totalHeuristic = round(distanceBetweenSuccAndStartCity+distanceBetweenSuccAndGoal,4)
                            successorValue = "".join(s_new)
                            if(randomList.get(initialVal) != None):
                                value = randomList[initialVal]
                                randomList[successorValue] = value + s + s_new
                            else:
                                randomList[successorValue] = [initialVal] + s_new
                            if is_goal(citySplit_new[0], endCity):
                                goalPath = randomList[initialVal]
                                goalPath = goalPath + s + s_new
                                randomList[initialVal] = goalPath
                                if(goalDictionary != None):
                                    goalDictionary.append(goalPath)
                                    return goalDictionary
                            else:
                                if(citySplit_new[0] not in visitedCities):
                                    fringe[totalHeuristic] = s_new
                                visitedCities.append(citySplit_new[0])
                     
                    else:
                        fringe[50.0] = s_new
                        visitedCities.append(citySplit_new[0])    

# ----A STAR SEARCH----
# Initial State = [startCity, endCity]
# Successor Function
# Heuristic Function = For any successor having multiple paths, choose the path which takes
# lesser time. We have no idea how far the goal is and therefore we assume that by travelling through
# nodes with lesser time, we will reach the goal in shortest time
# Final state = Path with shortest travelling time between the startCity and the endCity

# If a city A has a successor B which cannot be found in the city-gps file, then we try to find the successors of city B
# and then calculate the heuristic. Therefore, we assume that that city B does not exist even and therefore a straight road exists
# between city A and city C(successor of city B) 
def astartForTime(cities):
    startCity = cities[0]
    endCity = cities[1]
    fringe = {0: startCity}
    visitedCities = [startCity]
    goalDictionary = []
    randomList = {}
    
    while(len(fringe) > 0):
        initialValue = "".join(fringe[min(fringe)])
        for s in successors(popWithLeastValue(fringe)):
            citySplit = "".join(s).split(" ")
            time = heuristicForTime(citySplit)
            successorValue = "".join(s)
            
            if(randomList.get(initialValue) != None):
                value = randomList[initialValue]
                randomList[successorValue] = value + s
            else:
                randomList[successorValue] = [initialValue] + s
            if is_goal(citySplit[0], endCity):
                goalPath = randomList[initialValue]
                goalPath = goalPath + s
                randomList[initialValue] = goalPath
                if(goalDictionary != None):
                    goalDictionary.append(goalPath)
                    print(goalDictionary)
                    return goalDictionary
                
            if(citySplit[0] not in visitedCities):
                fringe[time] = s
            visitedCities.append(citySplit[0])

def heuristicForTime(citySplit):            
    distance = int(citySplit[1])
    speed = int(citySplit[2])
    if(speed == 0):
        speed = 1
    time = distance/speed
    
    return(round(time,4))

# ----A STAR SEARCH----
# Initial State = [startCity, endCity]
# Successor Function
# Heuristic Function = We have to find the path which spends lesser time on highways i.e paths
# with speed limit greater than 55. Now, we need to minimize our speed and maximize our distance
# because we need to spend the max time on roads with speed less than 55. Hence, by the formula
# our time will maximise. Hence, the heuristic function with maximised time.
# Final state = Path with lesser time spent on highways startCity and the endCity

# If a city A has a successor B which cannot be found in the city-gps file, then we try to find the successors of city B
# and then calculate the heuristic. Therefore, we assume that that city B does not exist even and therefore a straight road exists
# between city A and city C(successor of city B)    
def astarForScenic(cities):
    startCity = cities[0]
    endCity = cities[1]
    fringe12 = {0: startCity}    
    visitedCities = [startCity]
    randomList = {}
    goalDictionary = []
    
    while(len(fringe12) > 0):
        initialVal = "".join(fringe12[max(fringe12)])
        for s in successors(fringe12.pop(max(fringe12))):
            if(s != None):
                citySplit = "".join(s).split(" ")
                if(citySplit[0] not in visitedCities):
                    visitedCities.append(citySplit[0])
                    successorValue = "".join(s)
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                    if is_goal(citySplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        if(goalDictionary != None):
                            goalDictionary.append(goalPath)
                            print(goalDictionary)
                            return goalDictionary
                    if(citySplit[2] == '0' or citySplit[2] == ' '):
                        citySplit[2] = '50'
                    time = round(float(citySplit[1])/float(citySplit[2]),5)
                    fringe12[time] = s
                 
# ----ITERATIVE DEEPENING SEARCH----
# Initial state = [startCity, endCity]
# Successor Function = Pop the node(road segment) at the front i.e implement the fringe as a queue until the goal is reached
# and keep on appending on the fringe if the node is not a goal
# Goal State = A path from startCity to endCity
# Cost = Uniform cost of all the nodes

# It searches level by level. If it does not find the goal on the first level then it starts again
# and tries to find the goal by searching till next level and so on. It will try to find the goal
# at the lowest level and return the goal as soon as it finds one.       

# IDS will give the same path in all the cases of distance, time, segments and scenic because
# it will try to find the goal at the lowest level. Any kind of modification to this approach will
# actually direct us to the astar algorithm.           

def ids(cities):
    startCity = cities[0]
    endCity = cities[1]
    fringe = [startCity]
    flag = 1
    goalPath = idSearchAlgorithm(flag, fringe, endCity, startCity)
    while(type(goalPath) is int):
        fringe = [startCity]
        flag = 1 + goalPath
        goalPath = idSearchAlgorithm(flag, fringe, endCity, startCity)
    return [goalPath]
    
# ----THE ITERATIVE DEEPENING SEARCH ALGO----
    
def idSearchAlgorithm(flag, fringe, endCity, startCity):
    randomList = {}
    goalDictionary = []
    visitedCities = [startCity]
    flagFromSearchAlgo = 0
    for i in range(0, flag):
        initialVal = "".join(fringe[0])
        for s in successors(fringe.pop(0)):
            if(s != None):
                cityName = "".join(s).split(" ")
                if(cityName[0] == endCity or cityName[0] not in visitedCities):
                    flagFromSearchAlgo += 1
                    visitedCities.append(cityName[0])
                    successorValue = "".join(s)
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        
                        goalDictionary = goalPath
                        return goalDictionary
                    fringe.append(s)
    return flagFromSearchAlgo
        
def popWithLeastValue(fringe):
    return fringe.pop(min(fringe))

#----THE HEURISTIC FUNCTION OF CALCULATING THE EUCLIDEAN DISTANCE

def calculateEuclideanDistance(latitude1, longitude1, latitude2, longitude2):
    latitudeDist = float(latitude1) - float(latitude2)
    longitudeDist = float(longitude1) - float(longitude2)
    euclideanDist = (longitudeDist**2+latitudeDist**2)**0.5
    return(round(euclideanDist,4))

# ----CALCULATE THE DISTANCE OF THE PATH OF THE GOAL----
    
def distanceOfGoalPaths(goalPaths):
    for goals in goalPaths:
        distance = 0
        for values in goals:
            valueSplit = values.split(" ")
            if(len(valueSplit) > 1):
                distance += int(valueSplit[1])
        return distance
    
def calcDis(goalPaths):
    distance = 0
    for goals in goalPaths:
        goalSplit = goals.split(" ")
        if(len(goalSplit) > 1):
            distance += int(goalSplit[1])
    return distance

def calTime(goalPaths):
    for goals in goalPaths:
        time = 0
        speed= 0
        distance = 0
        finalTime = 0
        goalSplit = goals.split(" ")
        if(len(goalSplit) > 1):
            if(goalSplit[2] == " " or goalSplit[2] == "0" or goalSplit[2] == ""):
                goalSplit[2] = "50"
            speed = float(goalSplit[2])
            distance = float(goalSplit[1])
            if(speed != 0):
                time = distance/speed
            else:
                time = distance/1
            finalTime += time
    return round(finalTime,4)

def calScenic(goalPaths):
    count = 0
    speed = 0
    for goals in goalPaths:
        goalSplit = goals.split(" ")
        if(len(goalSplit) > 1):
            if(goalSplit[2] == " " or goalSplit[2] == "0" or goalSplit[2] == ""):
                goalSplit[2] = "50"
            speed = int(goalSplit[2])
            if(speed > 55):
                count += 1
    return count     

def calSegments(goalPaths):
    count = 0
    for goals in goalPaths:
        count += 1
    return count
   
# ----CALCULATE THE TIME OF THE PATH OF THE GOAL----   
        
def timeOfGoalPaths(goalPaths):
    for goals in goalPaths:
        time = 0
        speed= 0
        distance = 0
        finalTime = 0
        for values in goals:
            valueSplit = values.split(" ")
            if(len(valueSplit) > 1):
                if(valueSplit[2] == " " or valueSplit[2] == "0" or valueSplit[2] == ""):
                    valueSplit[2] = "50"
                speed = float(valueSplit[2])
                distance = float(valueSplit[1])
                if(speed != 0):
                    time = distance/speed
                else:
                    time = distance/1
                finalTime += time
        return round(finalTime,4)
    
# ----CALCULATE THE SEGMENTS OF THE PATH OF THE GOAL----
        
def segments(goalPaths):
    count = 0
    for goals in goalPaths:
        for values in goals:
            count += 1
        print("no. of segments are",count)
        
# ----PRINTING THE OUTPUT----
        
def printingFormat(goalPaths):
    distance = distanceOfGoalPaths(goalPaths)
    time = timeOfGoalPaths(goalPaths)
    outputString = ""
    outputString = str(distance) + " " + str(time) +" "
    finalPath = goalPaths[0]
    i=0
#        valStr = "".join(val).split(" ")
#        print(valStr[0])
#        i=1
#        if i==1:
#            valstr = val
            
        
    for goals in goalPaths:
        for values in goals:
            valueSplit = values.split(" ")
            strValue = "".join(valueSplit[0])
            outputString += strValue + " "
    print(outputString)            


# ---- Input Error Checking and correct calling of methods ----

dictionary = creatingADictionary()
commandLineArgs = readingFromCommandLine()
if(commandLineArgs[3] == None or commandLineArgs[2] == None):
    print("Routing option or algorithm cannot be empty! Exiting.\n")
    sys.exit()
if(commandLineArgs[3] == "bfs"):
    if(commandLineArgs[2] == "distance"):
        endCityValues = breadthFirstSearchForDistance(dictionary, commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "time"):
        endCityValues = breadthFirstSearchForTime(dictionary, commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "segments"):
        endCityValues = breadthFirstSearchForSegments(dictionary, commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "scenic"):
        endCityValues = breadthFirstSearchForScenic(dictionary, commandLineArgs)
        printingFormat(endCityValues)
    else:
        print("Invalid routing option entered! Exiting.\n")
        sys.exit()
elif(commandLineArgs[3] == "dfs"):
    if(commandLineArgs[2] == "distance"):
        endCityValues = depthFirstSearchForDistance(dictionary, commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "time"):
        endCityValues = depthFirstSearchForTime(dictionary, commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "segments"):
        endCityValues = depthFirstSearchForSegments(dictionary, commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "scenic"):
        endCityValues = depthFirstSearchForScenic(dictionary, commandLineArgs)
        printingFormat(endCityValues)
    else:
        print("Invalid routing option entered! Exiting.\n")
        sys.exit()
elif(commandLineArgs[3] == "ids"):
    if(commandLineArgs[2] == "distance"):
        endCityValues = ids(commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "time"):
        endCityValues = ids(commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "segments"):
        endCityValues = ids(commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "scenic"):
        endCityValues = ids(commandLineArgs)
        printingFormat(endCityValues)
    else:
        print("Invalid routing option entered! Exiting.\n")
        sys.exit()
elif(commandLineArgs[3] == "astar"):
    if(commandLineArgs[2] == "distance"):
        endCityValues = astarSearchForDistance(commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "time"):
        endCityValues = astartForTime(commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "segments"):
        endCityValues = ids(commandLineArgs)
        printingFormat(endCityValues)
    elif(commandLineArgs[2] == "scenic"):
        endCityValues = astarForScenic(commandLineArgs)
        printingFormat(endCityValues)
    else:
        print("Invalid routing option entered! Exiting.\n")
        sys.exit()
else:
    print("Invalid routing algorithm entered! Exiting.\n")       