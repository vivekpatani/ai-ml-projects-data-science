data = open("testdata")
# load the data from the file
print(data)

#data_list = data.split("\n")
data_dict = {}
for line in data:
    line_split_list = line.split()
    if line_split_list[0] in data_dict:
        data_dict[line_split_list[0]][line_split_list[1]] = line_split_list[2]
    else:
        data_dict[line_split_list[0]] = {line_split_list[1]:line_split_list[2]}

data.close()
