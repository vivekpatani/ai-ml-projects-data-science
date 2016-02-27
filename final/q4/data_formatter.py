import pickle
import json

def data_test():
    data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['reddit','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['reddit','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['reddit','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

    pickle.dump(data,open("./result/"+".p","wb"))
    #print(data)

    print("dumped")
    return data

def data_formatter(path,filename,destination,header):
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
            print(data[i])
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

    return data
    

def main():
    data_test()
    #header = ['sepal_length','sepal_width','petal_length','petal_width','class']
    #data_formatter("./data/","iris",header,"./result/")

if __name__ == "__main__":
    main()    
