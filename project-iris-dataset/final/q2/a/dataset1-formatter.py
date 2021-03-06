#Used for q-3
import csv

#To format the data
def data_formatter(path,filename,destination):

    input_file = open(path+filename+".data")
    format_string = ""

    for line in input_file:

        split_input = line.split()
        for i in range(len(split_input)):
            if i != 0:
                format_string = format_string+","+split_input[i]
            else:
                format_string = format_string+split_input[i]
        format_string += "\n"
    print(format_string)

    with open(destination+filename+'.csv','w') as output:
        output.write(format_string)
    output.close()

def main():
    data_formatter("./data/","wine","./results/")

if __name__ == "__main__":
    main()
