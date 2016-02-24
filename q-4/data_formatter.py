# -*- coding: utf-8 -*-
"""
@author: Vivek Patani
"""
import json
import pickle

def data_formatter(path,filename,header,destination,sep=","):

    #Use to load the file from the data directory
    input_file = open(path+filename+".data")
    
    #To init a simple data frame
    data = []
    
    #Append Header    
    
    #For each line in the input
    for line in input_file:
        
        #Add the data in a list to the data frame
        data.append((line.rstrip().split(",")))
        
        for i in range(len((data))):
            for j in range(len(data[i])-1):
                data[i][j] = float(data[i][j])
    
    
    #Appending header for reference    
    data.insert(0,header)
    
    #Closing the file
    input_file.close()
    
    #Store in pickel format
    pickle.dump(data,open(destination+filename+".p","wb"))
    
    #Just for future reference
    output = open(destination+filename+".json","w")
    json.dump(data,output,ensure_ascii=False,indent=4)
    output.close()
    
    #Debug
    print(data)
    

def main():
    header = ['sepal_length','sepal_width','petal_length','petal_width','class']
    data_formatter("./data/","iris",header,"./result/")

if __name__ == "__main__":
    main()