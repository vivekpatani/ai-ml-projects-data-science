# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 22:52:42 2016

@author: Vivek Patani
"""



from buildtree import *


def total_error(a,b):
    x = 

count=0
pes_er=1


def validation(rows):
    class_dict=group_by_counts(rows)
    #print(class_dict)
    total_error=sum([i for i in error.values() if i!=max(error.values())])
    #print("te is",te)
    global count
    pe=(total_error+ leafs_count*0.5)/float(150)
    return pe


def buildtree_validation(rows,score=entropy):
  

  if len(rows)==0: return node() 
    
    
  current_score=score(rows)

  error
  if count > 2:
        
        if validation_error(rows)<=pes_er:
            pes_er=pessimistic_error(rows)
        else:
            return decisionnode(results=uniquecounts(rows))
    
  

  gain_error=0.0
  best_criteria=None
  best_sets=None
  
  
  column_count=len(rows[0])-1
  for col in range(0,column_count):
    column_values={}
    for row in rows:
       column_values[row[col]]=1
    for value in column_values.keys():
      (set1,set2)=divideset(rows,col,value)
      
        error_gain=gain
        feature=(col,value)
        collect=(set1,set2)
 
      elif best_gain>0:
        trueBranch=buildtree_pessimistic(best_sets[0])
        falseBranch=buildtree_pessimistic(best_sets[1])
        return decisionnode(col=best_criteria[0],value=best_criteria[1],
          tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=group_by_count(rows)) 
