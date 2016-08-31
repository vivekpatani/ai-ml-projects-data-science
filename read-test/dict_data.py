import json
import io
import collections
from pprint import pprint

def main():
    data_dump()

user = 943
def data_dump():
    data = open('testdata')
    
    #data_list = data.split("\n")
    data_dict = {}
    for line in data:
        line_split_list = line.split()
        if line_split_list[0] in data_dict:
            data_dict[line_split_list[0]][line_split_list[1]] = int(line_split_list[2])
        else:
            data_dict[line_split_list[0]] = {line_split_list[1]:int(line_split_list[2])}


    #od = collections.OrderedDict(sorted(data_dict.items()))
    with open("udata.json","w") as outfile:
        json.dump(data_dict,outfile,ensure_ascii=False,indent=4)

if __name__ == '__main__':
    main()
