# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 22:52:42 2016

@author: Vivek Patani
"""



from buildtree import *


leafs_count=0
pes_er=1


def validation_error(rows):
    class_dict=uniquecounts(rows)
    #print(class_dict)
    te=sum([i for i in class_dict.values() if i!=max(class_dict.values())])
    #print("te is",te)
    global leafs_count
    pe=(te+ leafs_count*0.5)/float(150)
    return pe

'''
Building Tree from Generalize pessimistic error
approach i,e 'll stop growing tree once Generalize pessimisric error
starts growing for a branch
'''
from entropy import *
def buildtree_validation(rows,scoref=entropy):
  

  if len(rows)==0: return decisionnode() 
    
    
  current_score=scoref(rows)

  global pes_er
  global leafs_count
  #print("pessimistic error is",pes_er)
  #return decisionnode()
  if leafs_count > 2:
        #print("Here",len(rows))
        if validation_error(rows)<=pes_er:
            pes_er=pessimistic_error(rows)
        else:
            return decisionnode(results=uniquecounts(rows))
    
  

  # Set up some variables to track the best criteria
  best_gain=0.0
  best_criteria=None
  best_sets=None
  
  
  column_count=len(rows[0])-1
  for col in range(0,column_count):
    # Generate the list of different values in
    # this column
    column_values={}
    for row in rows:
       column_values[row[col]]=1
    # Now try dividing the rows up for each value
    # in this column
    
    for value in column_values.keys():
      (set1,set2)=divideset(rows,col,value)
      
      # Information gain
      p=float(len(set1))/len(rows)
      gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
      if gain>best_gain and len(set1)>0 and len(set2)>0:
        best_gain=gain
        best_criteria=(col,value)
        best_sets=(set1,set2)
 
  # Create the sub branches only if generalization error is not increased
      elif best_gain>0:
        trueBranch=buildtree_pessimistic(best_sets[0])
        falseBranch=buildtree_pessimistic(best_sets[1])
        return decisionnode(col=best_criteria[0],value=best_criteria[1],
          tb=trueBranch,fb=falseBranch)


    
  else:
    #count_leafs()
    global leafs_count
    leafs_count=leafs_count+1
    #print("leafs_count is",leafs_count)
    #checking pessimistic generalization error
    
    return decisionnode(results=uniquecounts(rows)) 
