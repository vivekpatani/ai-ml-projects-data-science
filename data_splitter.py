"""
Created on Fri Mar 04 17:42:50 2016
@author: Vivek Patani
"""
import os
import sys
import json
from datetime import date
import re
import time
from multiprocessing import Process

def read_line_by_line(path,filename,ext,destination,encoding="iso-8859-1",number_of_chunks=1):

    file = open(path+filename+ext,encoding=encoding)
    file_line = file.readlines()
    file.close()

    output = open(destination+filename+"_output.csv","w",encoding=encoding)
    count = 0
    og_count = 0
    page_id = 0
    date_rev = ""

    for each_line in iter(file_line):
        
        start = time.clock()
        #print(each_line)

        if "</page>" in each_line:
            #print(page_id)
            final_string = str(page_id) + "," + str(count) + "," + date_rev[0:-1]+"\n"
            #print(final_string)
            output.write(final_string)
            og_count = 0
            date_rev = ""
            count = 0
            final_string = ""
            
        if "<revision>" in each_line:
            count = count + 1
            
        if "<timestamp>" in each_line:
            datedata = each_line.rstrip().replace('>',' ').replace('<',' ').split()
            temp = datedata[1].replace('T',' ').split()
            date_rev = date_rev + temp[0] + "|"
            #print(temp[0])

        if "<id>" in each_line and og_count==0:
            og_count = 1
            each_id = each_line.rstrip().replace('>',' ').replace('<',' ').split()
            page_id = int(each_id[1])
            #print(int(each_id[1]))

    print("Output File Generated.")
    end = time.clock()
    print("Execution Time:"+str(end-start))


#The function to acquire the first x chunk size
def read_in_chunks(file_object, chunk_size=1024*1024):

    #Define the chunk size in multiples of MB
    chunk_size = chunk_size * 250
    
    #Lazy function (generator) to read a file piece by piece. Default chunk size: 1k.
    while True:

        data = file_object.read(chunk_size)

        #If it's the end then break
        if not data:
            break

        else:
            yield(data)
                
def data_gen(path,filename,encoding="iso-8859-1",destination="./data_chunks/",number_of_chunks=20):
    #To get the current working directory.
    print(os.getcwd())

    #File opening Command
    print(path+filename)
    file = open(path+filename,encoding="iso-8859-1")

    #Process to break the read file and store it in chunks
    counter = 0

    for piece in read_in_chunks(file):
    
        data = piece

        #counter for file number
        counter = counter + 1

        #Generating Filenames
        outf = "file" + str(counter) + ".xml"

        #Open the output file to write in it
        outfile = open(destination+outf,"w",encoding="iso-8859-1")
        outfile.write(piece)
        print(outf + " Generated.")
        outfile.close()

        #Cleaning up after each iteration
        outf = ""

        #Number of chunks needed
        #Comment if you need to the whole file to be broken
        if(counter == number_of_chunks):
            break

def json_data_extract(path,filename):

    #Defining a blank dictionary
    data = {}

    #File Loading Command
    with open(path+filename,encoding="iso-8859-1") as file:
        data = json.load(file)

    print(data[0])

    basedate = date(2006, 1, 1)
    for count in range(140):
        if(data[count]):
            for each_item in data[count]:
                if each_item == "revision":
                    time = data[count]["revision"]["timestamp"]
                    currentdate = date(int(time[0:4]),int(time[5:7]),int(time[8:10]))
                    delta = currentdate - basedate
                    print(data[count]["title"] + ": " +str(delta))

def json_data_list(path,filename):

    #Defining a data list
    data = []

    #File Loading Command
    with open(path+filename,encoding="iso-8859-1") as file:
        data = json.load(file)

    
def main():

    outf = ""
    path = ".\data_chunks\."
    filename = "file";
    ext = ".xml"
    for i in range(1,16):
        
##    p1 = Process(target = read_line_by_line("./data/","file1",".xml","./result/"))
##    p1.start()
##    p2 = Process(target = read_line_by_line("./data/","file2",".xml","./result/"))
##    p2.start()
##    p3 = Process(target = read_line_by_line("./data/","file3",".xml","./result/"))
##    p3.start()
##    p4 = Process(target = read_line_by_line("./data/","file4",".xml","./result/"))
##    p4.start()
##    p5 = Process(target = read_line_by_line("./data/","file5",".xml","./result/"))
##    p5.start()
    #Calling the file split chunk function
        data_gen('E:/Downloads/enwiki-20151201-pages-meta-current.xml/','enwiki-20151201-pages-meta-current.xml',"iso-8859-1","./data_chunks/",20)
    #json_data_extract("./","data.json")
    #read_line_by_line("./","file1",".xml")


#Standard Bolier Plate
if __name__ == "__main__":
    main()
