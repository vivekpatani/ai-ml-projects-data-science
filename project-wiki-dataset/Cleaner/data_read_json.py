import json

def load_dump(path,filename,encoding="iso-8859-1"):

    data = {}
    with open(path+filename,encoding=encoding) as output:
        data = json.load(output)
        print("Loaded")
        output.close()

    return data

def main():
    data = load_dump("./","data.json")
    for each_line in data:
        print(each_line)

if __name__ == "__main__":
    main()
