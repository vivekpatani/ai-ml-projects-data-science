import json
import time
#To find Pearson Correlation

#Method to iterate over each feature and find correlation
def data_scanner(path,filename,destination):

    #Just to calculate time
    start = time.clock()

    #Defining an empty dictionary
    data = {}
    computation_result = {}

    #Loading the data file
    with open(path+filename) as data_file:
        data = json.load(data_file)

    feature_list = ["type_of_wine","alcohol","malic_acid","ash","alcalinity_of_ash","magnesium","phenols","flavanoids","nonflavanoid_phenols","proanthocyanins","color_intensity","hue","dilution","proline"]
    list1 = []
    list2 = []
    pearson_coefficient = 0.0
    count = 1;

    for each in feature_list:
        #print(each)
        computation_result.setdefault(each,{})
        for other in feature_list:
            #print(other)
            if each!=other:
                for each_record in data:
                    list1.append(data[each_record][each])
                    list2.append(data[each_record][other])
                    #print(each+other)
                    pearson_coefficient = pearson_correlation_calc(list1,list2);
                    
                print("Pearson Correlation Between "+each+" & "+other+":"+str(pearson_coefficient))
                computation_result[each][other] = float(pearson_coefficient)

    with open(destination+"comparison"+".json",'w') as output:
        json.dump(computation_result,output,ensure_ascii=False,indent=4)

    print(destination+filename+".json Generated")
    print(time.clock() - start)
                

#Pearson Correlation Calculator
def pearson_correlation_calc(object1,object2):

    values = range(len(object1))

    #Finding the sum
    sum_object1 = sum([float(object1[i]) for i in values])
    sum_object2 = sum([float(object2[i]) for i in values])

    #Square of the sums
    square_sum1 = sum([pow(object1[i],2) for i in values])
    square_sum2 = sum([pow(object2[i],2) for i in values])

    #Adding the products
    product = sum([object1[i]*object2[i] for i in values])

    numerator = product - (sum_object1*sum_object2/len(object1))
    denominator = ((square_sum1 - pow(sum_object1,2)/len(object1)) * (square_sum2 - pow(sum_object2,2)/len(object1))) ** 0.5

    if denominator == 0:
        return 0

    result = numerator/denominator
    return result

#Data Formatter
def wine_formatter(path,filename,destination):

    #Defining an empty dictionary
    data = {}

    #Loading the data file
    data_file = open(path+filename)

    #Keeping count to maintain uniqueness
    count = 1
    
    #Iterating over each line in data file
    for each_line in data_file:

        #Defining a default structure for the dictionary
        data.setdefault(int(count),{})

        #Splitting the data and storing in JSON
        data_split = each_line.split(",")
        data[count]["type_of_wine"] = int(data_split[0])
        data[count]["alcohol"] = float(data_split[1])
        data[count]["malic_acid"] = float(data_split[2])
        data[count]["ash"] = float(data_split[3])
        data[count]["alcalinity_of_ash"] = float(data_split[4])
        data[count]["magnesium"] = float(data_split[5])
        data[count]["phenols"] = float(data_split[6])
        data[count]["flavanoids"] = float(data_split[7])
        data[count]["nonflavanoid_phenols"] = float(data_split[8])
        data[count]["proanthocyanins"] = float(data_split[9])
        data[count]["color_intensity"] = float(data_split[10])
        data[count]["hue"] = float(data_split[11])
        data[count]["dilution"] = float(data_split[12])
        data[count]["proline"] = float(data_split[13])

        count += 1

        #print(count)

    #Closing the file stream
    data_file.close()

    #Writitng the output to a JSON String.
    with open(destination+filename+'.json','w') as output_file:
        json.dump(data,output_file,ensure_ascii=False,indent=4)

    #Prompt to make sure file is successfully generated
    print("Output File Generated: "+filename+".json")

    #Closure and Clean Up
    output_file.close()
    data.clear()

def main():
    #wine_formatter("./data/","wine.data","./results/")
    data_scanner("./results/","wine.data.json","./results/")

if __name__ == "__main__":
    main()
