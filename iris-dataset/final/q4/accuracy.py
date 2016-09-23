from classifier import *
import pickle
from buildtree import *
#from buildtree_pessimistic import *
from printtree import * 
from sklearn.metrics import confusion_matrix

'''
Function to calculate accuracy of decision tree 
on 10 folds.
'''
def accuracy(filename):
	accuracyList=[]
	for iteration in range(1,11):
		
		subpath="./result/"+filename+"/"+filename
		
		train_data=pickle.load(open(subpath+"train"+str(iteration)+".p","rb"))
		tree=buildtree(train_data)
		test_data=pickle.load(open(subpath+"test"+str(iteration)+".p","rb"))
		correct=0
		comparison=0
		for each in test_data:
			comparison+= 1
			predicted_class=mdclassify(each,tree)
			if each[-1] == predicted_class:
				correct += 1
		test_accuracy=correct/float(comparison)
		accuracyList.append(test_accuracy)
	accuracy=sum(accuracyList)/float(10)
	print("Final Accuracy:"+str(accuracy*100))
	return accuracy*100