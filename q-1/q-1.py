import json
import math

#Method to format data and store in JSON Format to actually use it then
def data_formatter(path,filename,destination):

    #Opening the file
    data_file = open(path+filename)

    #Defining a basic Dictionary
    data = {}

    #Keeping a counter to count the number of objects    
    count = 1

    #For each line in the data file
    for each_line in data_file:

        #Defining a default structure for the data dictionary
        data.setdefault(count,{})

        #Splitting the data file
        split_data = each_line.split(",")
        data[count]["type"] = (split_data[4]).rstrip()
        data[count]["sepal_length"] = float(split_data[0])
        data[count]["sepal_width"] = float(split_data[1])
        data[count]["petal_length"] = float(split_data[2])
        data[count]["petal_width"] = float(split_data[3])

        #To show the count of data objcts parsed
        print(count);
        count += 1

    #Basic Data Closure
    data_file.close()

    #Writing to output in a JSON String.
    with open(destination+filename+'.json','w') as output:
        json.dump(data,output,ensure_ascii=False,indent=4)

    print("Output File Generated:" +filename+".json")

    #Closure and Clean up
    output.close()
    data.clear();
    
#Method to calculate the average of each feature
def calc_avg(path,filename,feature_name):

    #Defining a basic Dictionary
    data = {}
    
    #Opening the file
    with open(path+filename) as input_file:
        data = json.load(input_file)
    
    #Keeping a counter to count the number of objects    
    count = 0
    sum = 0.0
    average = 0.0

    #For each object in data
    for each in data:

        #Find the sum of the feature
        sum += data[each][feature_name]
        count += 1
        #print(count)

    #Calculate the Average
    average = round(float(sum/count),2)
    print("Average for "+feature_name+": "+str(average))

    #Clean Up
    input_file.close()
    data.clear()

    return average


def calc_sd(path,filename,feature_name):

    mean = calc_avg(path,filename,feature_name)

    #Defining a basic Dictionary
    data = {}
    
    #Opening the file
    with open(path+filename) as input_file:
        data = json.load(input_file)
    
    #Keeping a counter to count the number of objects    
    count = 0
    variance = 0.0
    standard_deviation = 0.0
    square = 0.0
    total = 0.0

    #For each object in data
    for each in data:

        #Find the sum of the feature
        term = mean - data[each][feature_name]
        square = term * term
        total = total + square
        count += 1
        square = 0.0
        term = 0.0
        #print(count)

    #Calculate the Average
    variance = round(float(total/count),2)
    print("Variance for "+feature_name+": "+str(variance))

    standard_deviation = math.sqrt(variance)
    print("Standard Deviation for "+feature_name+": "+str(standard_deviation))

    #Clean Up
    input_file.close()
    data.clear()

    return standard_deviation

def calc_avg_type(path,filename,feature_name,flower_type):

    #Defining a basic Dictionary
    data = {}
    
    #Opening the file
    with open(path+filename) as input_file:
        data = json.load(input_file)
    
    #Keeping a counter to count the number of objects    
    count = 0
    sum = 0.0
    average = 0.0

    #For each object in data
    for each in data:

        #Check for the particular Flower Type
        if(data[each]["type"] == flower_type):
            #Find the sum of the feature
            sum += data[each][feature_name]
            count += 1
            #print(count)

    #Calculate the Average
    average = round(float(sum/count),2)
    print("Average for "+feature_name+" & "+flower_type+": "+str(average))

    #Clean Up
    input_file.close()
    data.clear()

    return average


def calc_sd_type(path,filename,feature_name,flower_type):
    
    mean = calc_avg_type(path,filename,feature_name,flower_type)

    #Defining a basic Dictionary
    data = {}
    
    #Opening the file
    with open(path+filename) as input_file:
        data = json.load(input_file)
    
    #Keeping a counter to count the number of objects    
    count = 0
    variance = 0.0
    standard_deviation = 0.0
    square = 0.0
    total = 0.0

    #For each object in data
    for each in data:

        #For each flower type
        if data[each]["type"] == flower_type:

            #Find the sum of the feature
            term = mean - data[each][feature_name]
            square = term * term
            total = total + square
            count += 1
            square = 0.0
            term = 0.0
            #print(count)

    #Calculate the Average
    variance = round(float(total/count),2)
    print("Variance for "+feature_name+" & "+flower_type+": "+str(variance))

    standard_deviation = math.sqrt(variance)
    print("Standard Deviation for "+feature_name+" & "+flower_type+": "+str(standard_deviation))

    #Clean Up
    input_file.close()
    data.clear()

    return standard_deviation

def main():

    #In order to convert raw data to json file, to make it usable and readable
    #data_formatter("./data/","iris.data","./result/")

    #In order to calculate Average once data is formatted
    #calc_avg("./result/","iris.data.json","petal_width")
    #calc_avg("./result/","iris.data.json","petal_length")
    #calc_avg("./result/","iris.data.json","sepal_length")
    #calc_avg("./result/","iris.data.json","sepal_width")

    #In order to calculate Average, Variance and Standard Deviation
    #calc_sd("./result/","iris.data.json","petal_width")
    #calc_sd("./result/","iris.data.json","petal_length")
    #calc_sd("./result/","iris.data.json","sepal_length")
    #calc_sd("./result/","iris.data.json","sepal_width")

    #In order to calculate mean for each Flower Type with each feature
    #Setosa
    #calc_avg_type("./result/","iris.data.json","sepal_width","Iris-setosa")
    #calc_avg_type("./result/","iris.data.json","sepal_length","Iris-setosa")
    #calc_avg_type("./result/","iris.data.json","petal_width","Iris-setosa")
    #calc_avg_type("./result/","iris.data.json","petal_length","Iris-setosa")

    #Versicolor
    #calc_avg_type("./result/","iris.data.json","sepal_width","Iris-versicolor")
    #calc_avg_type("./result/","iris.data.json","sepal_length","Iris-versicolor")
    #calc_avg_type("./result/","iris.data.json","petal_width","Iris-versicolor")
    #calc_avg_type("./result/","iris.data.json","petal_length","Iris-versicolor")

    #Virginica
    #calc_avg_type("./result/","iris.data.json","sepal_width","Iris-virginica")
    #calc_avg_type("./result/","iris.data.json","sepal_length","Iris-virginica")
    #calc_avg_type("./result/","iris.data.json","petal_width","Iris-virginica")
    #calc_avg_type("./result/","iris.data.json","petal_length","Iris-virginica")

    #In order to calculate Standard Deviation for each Flower Type with each feature
    #Setosa
    calc_sd_type("./result/","iris.data.json","sepal_width","Iris-setosa")
    calc_sd_type("./result/","iris.data.json","sepal_length","Iris-setosa")
    calc_sd_type("./result/","iris.data.json","petal_width","Iris-setosa")
    calc_sd_type("./result/","iris.data.json","petal_length","Iris-setosa")

    #Versicolor
    calc_sd_type("./result/","iris.data.json","sepal_width","Iris-versicolor")
    calc_sd_type("./result/","iris.data.json","sepal_length","Iris-versicolor")
    calc_sd_type("./result/","iris.data.json","petal_width","Iris-versicolor")
    calc_sd_type("./result/","iris.data.json","petal_length","Iris-versicolor")

    #Virginica
    calc_sd_type("./result/","iris.data.json","sepal_width","Iris-virginica")
    calc_sd_type("./result/","iris.data.json","sepal_length","Iris-virginica")
    calc_sd_type("./result/","iris.data.json","petal_width","Iris-virginica")
    calc_sd_type("./result/","iris.data.json","petal_length","Iris-virginica")

if __name__ == "__main__":
	main()
