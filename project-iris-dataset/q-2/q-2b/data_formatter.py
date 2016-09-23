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
        data[count]["alcohol"] = float(split_data[0])
        data[count]["malic_acid"] = float(split_data[1])
        data[count]["ash"] = float(split_data[2])
        data[count]["alclinity_of_ash"] = float(split_data[3])
        data[count]["magnesium"] = float(split_data[4])
        data[count]["total_phenols"] = float(split_data[5])
        data[count]["flavanoids"] = float(split_data[6])
        data[count]["nonflavanoid_phenols"] = float(split_data[7])
        data[count]["proathocyanins"] = float(split_data[8])
        data[count]["color_intensity"] = float(split_data[9])
        data[count]["hue"] = float(split_data[10])
        data[count]["dilution"] = float(split_data[11])
        data[count]["proaline"] = float(split_data[12])

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
    data.clear()

def eucledian(path,filename,destination):

    data = {}
    q= 0.0

    with open(path+filename+".json") as input_file:
        data = json.load(input_file)

    for each_record in data:
        data.setdefault(each_record,{})
        for other_record in data:
            if(each_record!=other_record):
                q = float(calculate_eucledian(each_record,other_record))
                eucledian[each_record][other_record] = q

    with open(destination+filename+"eucledian.json","w") as out_file:
        json.dump(data,out_file,ensure_ascii=False,indent=4)

def calculate_eucledian(each,other):

    print(each,other)
    return 1
    
def main():

    #In order to convert raw data to json file, to make it usable and readable
    data_formatter("./data/","wine.data","./results/")
    eucledian("./results/","wine.data","./results/")

if __name__ == "__main__":
    main()
