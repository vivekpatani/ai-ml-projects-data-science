
import data_formatter
from collections import defaultdict
import entropy
from entropy import *
from buildtree import *
from printtree import *
from genkfolds import *
from classifier import mdclassify
from accuracy import *
from tst import *
from prune import *
from buildtree_validation import *

def main():
    header = ['sepal_length','sepal_width','petal_length','petal_width','class']
    #data_formatter("./data/","iris",header,"./result/")
    #header2 = pickle.load(open("./data/labels"+".p"))
    data = data_formatter.data_formatter("./data/","iris","./result/iris",header)
    #data2 = data_formatter.data_formatter("./data/","banknote","./result/banknote",header2)
    #tree2 = buildtree(data2)
    tree = buildtree(data)
    printtree(tree)
    #printtree(tree2)
    
    drawtree(tree=tree,jpeg="./result/iris/tree-iris.jpg",colname=data[0])
    #drawtree(tree=tree2,jpeg="./result/banknote/tree-banknote.jpg",colname=data2[0])
    genfolds("./result/","iris","./result/")
    #genfolds("./result/","banknote","./result/")
    #acc2 = accruacy("banknote")
    acc = accuracy("iris")
    #header2 = pickle.load(open("./data/labels"+".p"))
    #data2 = data_formatter.data_formatter("./data/","banknote","./result/banknote",header2)
    
    
if __name__ == "__main__":
    main()
