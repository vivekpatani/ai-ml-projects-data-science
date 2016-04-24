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
from os import listdir
from os.path import isfile, join

def call_read():
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def read_line_by_line(path,filename,ext,destination="./result/",encoding="iso-8859-1",number_of_chunks=1):

    file = open(path+filename+ext,encoding=encoding)
    file_line = file.readlines()
    file.close()

    output = open(destination+filename+"_output.csv","w",encoding=encoding)
    count = 0
    og_count = 0
    page_id = 0
    date_rev = ""
    data_desc_frame = []
    data_single_desc_frame = ""
    flag = False
    class_variable = False
    header = "page id" + "," + "Number of Revs" + "," + "last_date" + "," + "first_date" + "," + "Class" + "," + "2008" + "," + "2009" + "," + "2010" + "," + "2011" + "," + "2012" + "," + "2013" + "," + "2014" + "," + "2015" + "," + "2016" + "Upto_2012_Weights" + "," + "After_2013_Weights" + "\n"
    output.write(header)

    for each_line in iter(file_line):

        if "<text xml:space=\"preserve\">" in each_line:
            flag = True
        if "</text>" in each_line:
            data_desc_frame.append(data_single_desc_frame)
            data_single_desc_frame = ""
            flag = False
        
        start = time.clock()
        #print(each_line)

        if "</page>" in each_line:
            #print(data_desc_frame[0:])
            #print(page_id)

            if int(date_rev[:4]) >= 2008:
                class_variable = True
            else: class_variable = False

            c2008 = 0
            c2008 = date_rev.count('2008')

            c2009 = 0
            c2009 = date_rev.count('2009')

            c2010 = 0
            c2010 = date_rev.count('2010')

            c2011 = 0
            c2011 = date_rev.count('2011')

            c2012 = 0
            c2012 = date_rev.count('2012')

            c2013 = 0
            c2013 = date_rev.count('2013')

            c2014 = 0
            c2014 = date_rev.count('2014')

            c2015 = 0
            c2015 = date_rev.count('2015')

            c2016 = 0
            c2016 = date_rev.count('2016')

            sum_upto_2012 = c2008 + c2009 + c2010 + c2011 + c2012
            weighted_sum_2012 = sum_upto_2012 * 0.25
            
            sum_after_2016 = c2013 + c2014 + c2015 + c2016
            weighted_sum_2016 = sum_after_2016 * 0.75

            final_string = str(page_id) + "," + str(count) + "," + date_rev[-11:-1] + "," + date_rev[:10] + "," + str(class_variable) + "," +str(c2008) + "," +str(c2009) + "," +str(c2010) + "," +str(c2011) + "," +str(c2012) + "," +str(c2013) + "," +str(c2014) + "," +str(c2015) + "," +str(c2016) + ","+ str(weighted_sum_2012) + "," + str(weighted_sum_2016) + "\n"
            data_desc_frame = []
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

        if flag:
            data_single_desc_frame += each_line.rstrip()

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
    file = open(path+filename,encoding=encoding)

    #Process to break the read file and store it in chunks
    counter = 0

    for piece in read_in_chunks(file):
    
        data = piece

        #counter for file number
        counter = counter + 1

        #Generating Filenames
        outf = "file" + str(counter) + ".xml"

        #Open the output file to write in it
        outfile = open(destination+str(outf),"w",encoding=encoding)
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
    with open(path+filename,encoding=encoding) as file:
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
    with open(path+filename,encoding=encoding) as file:
        data = json.load(file)

    
def main():

    outf = ""
    path = ".\data_chunks\."
    filename = "file";
    ext = ".xml"
    for i in range(1,8):
        
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
    #data_gen('./input/','enwiki-20160305-pages-meta-history19.xml','iso-8859-1','data_chunks/',20)
    #json_data_extract("./","data.json")
        read_line_by_line("./data_chunks/","file"+str(i),".xml",encoding="iso-8859-1")


#Standard Bolier Plate
if __name__ == "__main__":
    main()
