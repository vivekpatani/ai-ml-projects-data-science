# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:20:32 2016

@author: Vivek Patani
"""

from sklearn.cross_validation import StratifiedKFold
from sklearn.cross_validation import StratifiedShuffleSplit
import pickle
from collections import Counter
import json
import os

import pickle

def getunique(row):
    
    uniqueItems = set(row)
    uniqueItems = list(uniqueItems)
    while "class" in uniqueItems: uniqueItems.remove("class")
    return int(len(uniqueItems)),uniqueItems
    
def genfolds(path,filename,destination):
    
    setNumber = 0
    data = {}
    data_file = pickle.load(open(path+filename+".p"))

    print(data_file)
    #Loading the class list (only if the last column is class)
    class_list = [each_row[len(each_row)-1] for each_row in data_file]

    while "class" in class_list: class_list.remove("class")
    
    #Getting the count and the unique labels present
    countLabel,label = getunique(each_row[len(each_row)-1] for each_row in data_file)

    #Only testing
    print (countLabel,label)

    count = 0;
    for each in label:
    	data[label[count]] = count
    	count += 1

    #if(countLabel!=len(list(set(class_list)))):
    	#print("Class List is not consistent.")
    	#return 0

    print(data)

    #To store their equivalent class lists
    class_data = []
    for each_class in class_list:
    	class_data.append(data[each_class])

    print(class_data)

    stratifiedKFoldOut = StratifiedKFold(class_data, 10)

    if not os.path.exists(destination+filename):
    	os.makedirs(destination+filename)
    destination = destination + filename + "/"

    for train,test in stratifiedKFoldOut:
        train_data = []
        test_data = []

    	setNumber+=1
    	for train_index in train:
    		train_data.append(data_file[train_index])

    	with open(destination+filename+"train"+str(setNumber)+".json","w") as output_file:
    		json.dump(train_data,output_file,ensure_ascii=False,indent=4)

    	pickle.dump(train_data,open(destination+filename+"train"+str(setNumber)+".p","wb"))

    	for train_index in train:
    		train_data.append(data_file[train_index])

    	with open(destination+filename+"test"+str(setNumber)+".json","w") as output_file:
    		json.dump(train_data,output_file,ensure_ascii=False,indent=4)

    	pickle.dump(train_data,open(destination+filename+"test"+str(setNumber)+".p","wb"))
     

def main():
    
    genfolds("./result/","iris","./result/")
    
    #Only for testing
    #print(getunique([1,2,3,4,1,2,3,4,1,2,3,4]))

if __name__ == "__main__":
    main()
    