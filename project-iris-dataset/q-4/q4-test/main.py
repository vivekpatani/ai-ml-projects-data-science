
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
import pickle

def main():
#    header = ['sepal_length','sepal_width','petal_length','petal_width','class']
#    data = data_formatter.data_formatter("./data/","iris","./result/iris",header)
#    tree = buildtree(data)
#    printtree(tree)
#    drawtree(tree=tree,jpeg="./result/iris/tree-iris.jpg",colname=data[0])
#    genfolds("./result/","iris","./result/")
#    acc = accuracy("iris")
#    prune(tree)
#    drawtree(tree=tree,jpeg="./result/iris/tree-prune-iris.jpg",colname=data[0])
#    print("header")    
#    header_file = open("./data/banknote/header.p")
#    header2 = pickle.load(header_file)
#    print("header2")
#    #data2 = data_formatter.data_formatter("./data/","banknote","./result/banknote",header2)
#    data_file = open("./data/banknote/data.p")
#    data2 = pickle.load(data_file)
#    print("header3")
#    tree2 = buildtree(data2)
#    print("header44")
#    printtree(tree2)
#    print("header45")
#    drawtree(tree=tree2,jpeg="./result/banknote/tree-banknote.jpg",colname=data2[0])
#    print("header5")
#    genfolds("./result/","banknote","./result/")
#    acc = accuracy("banknote")
#    tree2 = prune(tree2)
#    drawtree(tree=tree2,jpeg="./result/banknote/tree-banknote-iris.jpg",colname=data2[0])
#    print("header")
#    header3 = "./data/banknote/header-c.p"    
#    print("header3")
#    data2 = data_formatter.data_formatter("./data/","car","./result/car",header3)
#    print("header3")
#    tree2 = buildtree(data3)
#    print("header44")
#    printtree(tree3)
#    print("header45")
#    drawtree(tree=tree3,jpeg="./result/car/tree-car.jpg",colname=data[0])
#    print("header5")
#    genfolds("./result/","car","./result/")
#    acc = accuracy("car")
#    tree2 = prune(tree2)
#    drawtree(tree=tree2,jpeg="./car/banknote/tree-car.jpg",colname=data[0])
#    
#    print("header")    
#    header_file = open("./data/haberman/header.p")
#    header2 = pickle.load(header_file)
#    print("header2")
#    #data2 = data_formatter.data_formatter("./data/","banknote","./result/banknote",header2)
#    data_file = open("./data/haberman/data.p")
#    data2 = pickle.load(data_file)
#    print("header3")
#    tree2 = buildtree(data2)
#    print("header44")
#    printtree(tree2)
#    print("header45")
#    drawtree(tree=tree2,jpeg="./result/haberman/tree-haberman.jpg",colname=data2[0])
#    print("header5")
#    genfolds("./result/","haberman","./result/")
#    acc = accuracy("haberman")
#    tree2 = prune(tree2)
#    drawtree(tree=tree2,jpeg="./result/haberman/haberman.jpg",colname=data2[0])
#    print("header")

    print("header")   
    header_file = open("./data/wine/header.p")
    header2 = pickle.load(header_file)
    print("wine")
    #data2 = data_formatter.data_formatter("./data/","banknote","./result/banknote",header2)
    data_file = open("./data/wine/data.p")
    data2 = pickle.load(data_file)
    print("header3")
    tree2 = buildtree(data2)
    print("header44")
    printtree(tree2)
    print("header45")
    drawtree(tree=tree2,jpeg="./result/wine/tree-wine.jpg",colname=data2[0])
    print("header5")
    genfolds("./result/","wine","./result/")
    acc = accuracy("wine")
    tree2 = prune(tree2)
    drawtree(tree=tree2,jpeg="./result/wine/wine.jpg",colname=data2[0])
    print("header")


if __name__ == "__main__":
    main()
