#Used for q-3-a
import csv

#To format the data
def data_formatter(path,filename,destination):
    i = 0
    input_file = open(path+filename)
    format_string = "age,workclass,fnlwgt,education,marital-status,occupation,relationship,race,sex,capital-gain,capital-loss,hours-per-week,native-country\n"

    for line in input_file:

        split_input = line.split(",")
        for i in range(len(split_input)):
            if i != 0:
                format_string = format_string+","+split_input[i]
            else:
                format_string = format_string+split_input[i]
        #format_string += "\n"
    print(format_string)
    print(i)

    with open(destination+filename+'.txt','w') as output:
        output.write(format_string)
    output.close()

def main():
    data_formatter("./data/","adult.data","./results/")

if __name__ == "__main__":
    main()
