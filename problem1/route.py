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
    return [start_city,end_city]

class node(object):
    visited = False
    recordPath = None
    
    def __init__(self, recordPath):
        self.visited = True
        self.recordPath = recordPath
    
parentNode = node
currentNode = ""

    
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

'''def checkingForEndCity(dictionary, cities):
    startCity = cities[0]
    endCity = cities[1]
    
    for i in range(0,len(dictionary[startCity])):
        stringSplit = "".join(dictionary[startCity][i]).split(" ")
        if(stringSplit[0] == cities[1]):
            return stringSplit
    return None'''

fringeVal = []

def successors(nextNode):
    #print(nextNode)
    inside = "".join(nextNode).split(" ")
    #print(inside[0])
    #for i in range(0,len(dictionary[nextNode])):
    #inside = "".join(nextNode).split(" ")
    #print(inside)
    if(not (dictionary.get(inside[0]))):
        return [None]
    return [dictionary[inside[0]][i] for i in range(0,len(dictionary[inside[0]]))]
            


readingFromCommandLine()
startCity = readingFromCommandLine()
dictionary = creatingADictionary()

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
    visitedCities = [startCity]
            
    while(len(fringe) > 0):
        initialVal = "".join(fringe[0])
        for s in successors(fringe.pop(0)):
            #print(s)
            #if (randomList.get(initialVal)):
            #for key in randomList:
                #valueOfKey = randomList[key]
                #if(valueOfKey != None):
                    #string12 = "".join(valueOfKey).split("-->")
                    #for i in range(0,len(string12)):
                        #if(string12[i] == "".join(initialVal)):
                            #randomList["".join(initialVal)] = [key+string12[i]+"".join(s)]
                            #print(randomList)
                #print("key",key," value of key",valueOfKey)
            #if(randomList.get("".join(initialVal))):
                #value = randomList.get("".join(initialVal))
                #newValue = "".join(value) +"-->"+ "".join(s)
                #randomList["".join(initialVal)] = [newValue]
            #else:
                #randomList["".join(initialVal)] = s

            
            if(s != None):
                cityName = "".join(s).split(" ")
                if(any(cityName[0] in value for word in fringe for value in word) or cityName[0] not in visitedCities):
                    if(not(cityName[0] == endCity)):
                        visitedCities.append(cityName[0])
                    successorValue = "".join(s)
                    if(randomList.get(initialVal) != None):
                        value = randomList[initialVal]
                        randomList[successorValue] = value + s
                    else:
                        randomList[successorValue] = [initialVal] + s
                
                    stringSplit = "".join(s).split(" ")
                    #print(stringSplit[0])
                    if is_goal(stringSplit[0], endCity):
                        goalPath = randomList[initialVal]
                        goalPath = goalPath + s
                        randomList[initialVal] = goalPath
                        if(goalDictionary != None):
                            goalDictionary.append(goalPath)
                        else:
                            goalDictionary = goalPath
                        print("Goal path is",randomList[initialVal] )
                        #return(s)
                    if(cityName[0] != endCity):
                        fringe.append(s)
    #print("random",randomList)
    print("the goal dictionary",goalDictionary)
    return goalDictionary
'''    for i in range(0, len(dictionary[startCity])):
        stringSplit = "".join(dictionary[startCity][i]).split(" ")
        if(stringSplit[0] == cities[1]):
            return stringSplit
        else:
            fringe.append(stringSplit[0])
            print(stringSplit[0])
            for s in successors(fringe.pop(0), cities[1]):
                print(s)
            #print(successors(fringe.pop(0)))
            print(fringe)'''

def distanceOfGoalPaths(goalPaths):
    for goals in goalPaths:
        distance = 0
        for values in goals:
            valueSplit = values.split(" ")
            if(len(valueSplit) > 1):
                distance += int(valueSplit[1])
        print("distance of goal path " +"".join(goals)+ "is ", distance)
        
def timeOfGoalPaths(goalPaths):
    for goals in goalPaths:
        time = 0
        speed= 0
        distance = 0
        finalTime = 0
        for values in goals:
            valueSplit = values.split(" ")
            if(len(valueSplit) > 1):
                speed = int(valueSplit[2])
                distance = int(valueSplit[1])
                time = distance/speed
                finalTime += time
        #time = distance / speed
        print("time of goal path " + "".join(goals)+ "is ", finalTime)
        
def segments(goalPaths):
    count = 0
    for goals in goalPaths:
        for values in goals:
            count += 1
        print("no. of segments are",count)
            
endCityValues = breadthFirstSearch(dictionary, startCity)
if(endCityValues is not None and endCityValues):
    print("path found")
else:
    print("No direct path")
    
distanceOfGoalPaths(endCityValues)
timeOfGoalPaths(endCityValues)
segments(endCityValues)
