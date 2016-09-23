import xml.etree.ElementTree as etree
 
times = []
keys = []
 
def main():
    tree = etree.parse('./data_chunks/file3.xml')
    for neighbor in root.iter('page'):
        print (neighbor.attrib)

    print(root)
 
if __name__ == "__main__": main()
