'''
Created on Sep 16, 2016

@author: Rohil
'''
import sys

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

def successors(nextNode):
    inside = "".join(nextNode).split(" ")
    if(not (dictionary.get(inside[0]))):
        return [None]
    return [dictionary[inside[0]][i] for i in range(0,len(dictionary[inside[0]]))]

def is_goal(node, endCity):
    if(node == endCity):
        return True
    return False

def breadthFirstSearch(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = []
            
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
                        print("Goal path is",randomList[initialVal] )
                        break
                    fringe.append(s)
                    
def depthFirstSearch(dictionary, cities):
    fringe=[]
    startCity = cities[0]
    endCity = cities[1]
    fringe.append(startCity)
    randomList = {}
    goalDictionary = []
    visitedCities = []
            
    while(len(fringe) > 0):
        initialVal = "".join(fringe[len(fringe)-1])
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
                        print("Goal path is",randomList[initialVal] )
                        break
                    fringe.append(s)
                    
                    

    print("the goal dictionary",goalDictionary)
    return goalDictionary

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

'''def astartForTime(cities):
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
            visitedCities.append(citySplit[0])'''

def heuristicForTime(citySplit):            
    distance = int(citySplit[1])
    speed = int(citySplit[2])
    if(speed == 0):
        speed = 1
    time = distance/speed
    
    return(round(time,4))
    
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
                    #if(fringe12.get(citySplit[2]) != None):
                    #    value = fringe12[citySplit[2]]
                    #   valueSplit = "".join(value).split(" ")
                        #if(int(valueSplit[2]) < 55):
                        #    if(valueSplit[1] > citySplit[1]):
                         #       fringe12[citySplit[2]] = value
                          #  else:
                           #     fringe12[citySplit[2]] = s
                        #else:
                        #    if(valueSplit[1] < citySplit[1]):
                        #        fringe12[citySplit[2]] = value
                        #    else:
                        #        fringe12[citySplit[2]] = s
                    #else:
                    if(citySplit[2] == '0' or citySplit[2] == ' '):
                        citySplit[2] = '50'
                    time = round(float(citySplit[1])/float(citySplit[2]),5)
                    fringe12[time] = s
                 

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

def calculateEuclideanDistance(latitude1, longitude1, latitude2, longitude2):
    latitudeDist = float(latitude1) - float(latitude2)
    longitudeDist = float(longitude1) - float(longitude2)
    euclideanDist = (longitudeDist**2+latitudeDist**2)**0.5
    return(round(euclideanDist,4))
    
def distanceOfGoalPaths(goalPaths):
    for goals in goalPaths:
        distance = 0
        for values in goals:
            valueSplit = values.split(" ")
            if(len(valueSplit) > 1):
                distance += int(valueSplit[1])
        #print("distance of goal path " +"".join(goals)+ "is ", distance)
        return distance
        
def timeOfGoalPaths(goalPaths):
    for goals in goalPaths:
        time = 0
        speed= 0
        distance = 0
        finalTime = 0
        for values in goals:
            valueSplit = values.split(" ")
            if(len(valueSplit) > 1):
                speed = float(valueSplit[2])
                distance = float(valueSplit[1])
                if(speed != 0):
                    time = distance/speed
                else:
                    time = distance/1
                finalTime += time
        #print("time of goal path " + "".join(goals)+ "is ", finalTime)
        return round(finalTime,4)
        
def segments(goalPaths):
    count = 0
    for goals in goalPaths:
        for values in goals:
            count += 1
        print("no. of segments are",count)
        
def printingFormat(goalPaths):
    distance = distanceOfGoalPaths(goalPaths)
    time = timeOfGoalPaths(goalPaths)
    outputString = ""
    outputString = str(distance) + " " + str(time) +" "
    for goals in goalPaths:
        for values in goals:
            valueSplit = values.split(" ")
            strValue = "".join(valueSplit[0])
            outputString += strValue + " "
    print(outputString)            


readFromGPSFile()  

readingFromCommandLine()
commandLineArgs = readingFromCommandLine()
dictionary = creatingADictionary() 

#if(commandLineArgs[3] == "bfs"):
#    endCityValues = breadthFirstSearch(dictionary, commandLineArgs)
#    printingFormat(endCityValues)
#if(endCityValues is not None and endCityValues):
#    print("path found")
#else:
#    print("No direct path")
    
#distanceOfGoalPaths(endCityValues)
#timeOfGoalPaths(endCityValues)
#segments(endCityValues)
astarValues = astarSearchForDistance(commandLineArgs)
printingFormat(astarValues)
#distanceOfGoalPaths(astarValues)
#timeOfGoalPaths(astarValues)
#segments(astarValues)

#dfsVal = depthFirstSearch(dictionary, startCity)
#distanceOfGoalPaths(dfsVal)

#idsValues = ids(startCity)

#distanceOfGoalPaths(idsValues)

#aStarTimeVal = astartForTime(startCity)
#timeOfGoalPaths(aStarTimeVal)

#astarScenicVal = astarForScenic(startCity)
#distanceOfGoalPaths(astarScenicVal)