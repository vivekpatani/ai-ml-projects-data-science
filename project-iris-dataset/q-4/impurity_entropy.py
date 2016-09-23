# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 01:48:17 2016

@author: Vivek Patani
"""

#Calculating Gini Impurity Here

from math import log
#Return 0 if length is 0
def giniimpurity(rows):
  if ((len(rows))==0):
    return 0
    total=len(rows)
    counts={}
    
    counts = group_by_count(rows)
    for item in rows:
        counts.setdefault(item,0)
        item += 1
        counts[item]
    impurity = 0
    for j in rows:
      f1=float(counts[j])/total
      for k in rows:
        if j==k: continue
        f2=float(counts[k])/total
        impurity+=f1*f2
  return impurity
 
def group_by_count(rows):
    results = defaultdict(lambda: 0)
    for row in rows:
        r = row[len(row)-1]
        results[r]+=1
    return dict(results) 

def entropy(rows):
    #Return 0 if length is 0
    if (len(rows)==0):
      return 0
    log2=lambda x:log(x)/log(2)
    results=group_by_counts(rows)

    # Now calculate the entropy for row
    entropy=0.0
    for r in results.keys():
      p=float(results[r])/len(rows)
      entropy=entropy-p*log2(p)
    return entropy

#calculate variance if class variable is numerical
def variance(rows):
  if len(rows)==0: return 0
  data=[float(row[len(row)-1]) for row in rows]
  mean=sum(data)/len(data)
  variance=sum([(d-mean)**2 for d in data])/len(data)
  return variance

def variance(rows):
  if len(rows)==0:
      return 0
  
  data=[float(row[len(row)-1]) for row in rows]
  mean=sum(data)/len(data)
  variance=sum([(d-mean)**2 for d in data])/len(data)
  return variance  