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
def accuracy10Fold(dataset=None,path="./Data"):
	
    # Training & Testing on corresponding Train Test pair.
	accuracyList=[]
	for f in range(1,11):
		#print("Building model from Training fold ",f)
		foldPath="./result/iris/iris"
		
		#Loading trainFold
		trainFoldData=pickle.load(open(foldPath+"train"+str(f)+".p","rb"))
		#trainFoldData=pickle.load(open("./Data/iris/folds/trainFold_1.p","rb"))
		
		#making normal decision Tree on this trainFold
		tree=buildtree(trainFoldData)
		

		#making pessimistic decision tree on this trainfold
		'''
		tree=buildtree_pessimistic(trainFoldData)
		'''

		'''
		writepath_pes=path+ "/"+ dataset + "/treeview_pes_" +str(f)+ ".jpg"
		colname=['sepal_length','sepal_width','petal_length','petal_width']
		drawtree(tree=tree,jpeg=writepath_pes,colname=colname)
		'''

		#print("Testing model for Testing fold",f)
		#Loading tesfold to check accuracy of the model
		testFoldData=pickle.load(open(foldPath+"test"+str(f)+".p","rb"))
		
		# Checking target class for each observation in test fold
		trueMatch=0
		totalCmp=0
		actual=[]
		predictions=[]
		for obs in testFoldData:
			#print(f)
			#print("obs is",obs)
			totalCmp=totalCmp+1
			result=mdclassify(obs,tree)
			#print("outcome is",result)
			#print (obs[-1],result)
			#if obs[-1] == result.keys()[0]: #i,e Target class is predicted correctly
			actual.append(obs[-1])
			predictions.append(result)
			if obs[-1] == result:
				trueMatch=trueMatch+1
		accuracy=trueMatch/float(totalCmp)
		print("Accuracy for Testing fold",f ,accuracy)
		accuracyList.append(accuracy)
		#print(accuracyList)
	finalAccuracy=sum(accuracyList)/float(10)
	print("Final Accuracy of " ,dataset,finalAccuracy)
	return finalAccuracy