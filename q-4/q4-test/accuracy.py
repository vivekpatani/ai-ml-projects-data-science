# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 01:51:32 2016

@author: Vivek Patani
"""

from classifier import *
import pickle
from buildtree import *
#from buildtree_pessimistic import *
from printtree import * 
from sklearn.metrics import confusion_matrix

def accuracy10Fold(filename,path="./Data"):
	
    #Training & Testing on corresponding Train Test pair.
	accuracyList=[]
	for count in range(1,11):
		test_data = pickle.load(open("./result/iris/"+filename+"test"+str(count)+".p","rb"))
		train_data = pickle.load(open("./result/iris/"+filename+"train"+str(count)+".p","rb"))
        tree = buildtree(train_data)

        comparison = 0
        correct = 0
        incorrect = 0
        original = []
        calculated = []
        for each_record in test_data:

        	#print(each_record)
        	comparison = comparison + 1
        	predicted_class = mdclassify(each_record,tree)
        	original.append(each_record[-1])
        	calculated.append(predicted_class)
        	if each_record[-1] == predicted_class:
        		correct += 1
        		print(correct,each_record)
        	else:
        		incorrect += 1

        accuracy = correct / float(comparison)
        accuracyList.append(accuracy)
        print(accuracyList)

	finalAccuracy=sum(accuracyList)/float(10)
	print("Final Accuracy of "+str(finalAccuracy))
	return finalAccuracy