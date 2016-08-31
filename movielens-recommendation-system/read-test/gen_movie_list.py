import json
import collections

def main():
    data_dump()

def data_dump():
    data = open('.\data\u.item');

    data_dict = {}
    for line in data:
        line_split_list = line.split('|')
        data_dict[line_split_list[0]] = line_split_list[1]
        print("Done"+line_split_list[0])

    with open("udata_movie.json","w") as outfile:
        json.dump(data_dict,outfile,ensure_ascii=False,indent=4)

    with open("udata_movie.json") as data_file:
        temp_data = json.load(data_file)

if __name__ == "__main__":
    main()
