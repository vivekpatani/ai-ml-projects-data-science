# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 14:35:15 2016

@author: Vivek Patani
"""
import data_formatter
import build
import divide
import impurity_entropy
import node
import drawtree

import pickle

def main():
    
    filepath = "./result/iris.p"
    destpath = "./result/"    
    
    header = ['sepal_length','sepal_width','petal_length','petal_width','class']
    data_formatter.data_formatter("./data/","iris",header,"./result/")
    
    data=pickle.load(open(filepath,"rb"))    
    tree=build.buildtree(rows=data[1:len(data)],no_leafnode=1)
    
    drawtree(tree=tree,jpeg=destpath,colname=data[0]) 
    writepath = destpath + "/treeview_prune.jpg"

    #divide.divideset(data,1,)
    
if __name__ == "__main__":
    main()