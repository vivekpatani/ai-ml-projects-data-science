# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 02:44:07 2016

@author: Vivek Patani
"""
def divideset(rows,column,value):
    
    # Make a function that tells us if a row is in the first group (true) or the second group (false)
    split_function=None
    
    # for numerical values
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    
    # for nominal values
    else:
        split_function=lambda row:row[column]==value
   
    # Divide the rows into two sets and return them
    set1=[row for row in rows if split_function(row)] # if split_function(row) 
    set2=[row for row in rows if not split_function(row)]
    
    #Returning the split list(sets)
    return (set1,set2)