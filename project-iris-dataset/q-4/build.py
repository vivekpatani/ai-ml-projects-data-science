# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 03:00:54 2016

@author: Vivek Patani
"""
from impurity_entropy import *
import divide as div
import node

def buildtree(rows, score=entropy):
    if len(rows) == 0: return node.decisionnode()
    current_score = score(rows)
    
    #Variables required
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    
    #Storing the result
    column_count = len(rows[0]) - 1	# last column is result
    for col in range(0, column_count):
        #find different values in this column
        column_values = set([row[col] for row in rows])

        # for each possible value, try to divide on that value
        for value in column_values:
            set1, set2 = div.divideset(rows, col, value)

            # Information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p*score(set1) - (1-p)*score(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return node.decisionnode(col=best_criteria[0], value=best_criteria[1],
                tb=trueBranch, fb=falseBranch)
    else:
        return node.decisionnode(results=imp.group_by_count(rows))

