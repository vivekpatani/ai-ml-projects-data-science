
import data_formatter
import divide
from collections import defaultdict
import entropy
from entropy import *
from buildtree import *
from printtree import *
from genkfolds import *
from classifier import mdclassify
from accuracy import *

def main():
    header = ['sepal_length','sepal_width','petal_length','petal_width','class']
    #data_formatter("./data/","iris",header,"./result/")
    data = data_formatter.data_formatter("./data/","iris","./result/iris",header)
    #set1,set2 = divide.divideset(data,1,'USA')
    #print("Set 1:",set1)
    #print("Set 2:",set2)
    #print(group_by_count(data))
    #print(entropy(set2))
    tree = buildtree(data)
    printtree(tree)
    drawtree(tree=tree,jpeg="./result/iris/tree-iris.jpg",colname=data[0])
    genfolds("./result/","iris","./result/")

    acc = accuracy10Fold("iris","./result/")

if __name__ == "__main__":
    main()
