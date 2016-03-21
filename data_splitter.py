"""
Created on Fri Mar 04 17:42:50 2016
@author: Vivek Patani
"""
import os
import sys
import json
from datetime import date

#The function to acquire the first x chunk size
def read_in_chunks(file_object, chunk_size=1024*1024):

    #Define the chunk size in multiples of MB
    #chunk_size = chunk_size * 25
    
    #Lazy function (generator) to read a file piece by piece. Default chunk size: 1k.
    while True:

        data = file_object.read(chunk_size)

        #If it's the end then break
        if not data:
            break

        else:
            yield(data)
            
def data_gen(path,filename,encoding="iso-8859-1",number_of_chunks=1):
    #To get the current working directory.
    print(os.getcwd())

    #File opening Command
    file = open(path+filename,encoding="iso-8859-1")

    #Process to break the read file and store it in chunks
    counter = 0
    for piece in read_in_chunks(file):
        data = piece

        #counter for file number
        counter = counter + 1

        #Generating Filenames
        outf = "file" + str(counter) + ".xml"
        print(outf + "Generated.")

        #Open the output file to write in it
        outfile = open(outf,"w",encoding="iso-8859-1")
        outfile.write(piece)

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

    #Calling the file split chunk function
    #data_gen("enwikiquote-20160203-pages-articles-multistream.xml/","enwikiquote-20160203-pages-articles-multistream.xml","iso-8859-1",1)
    json_data_extract("./","data.json")


#Standard Bolier Plate
if __name__ == "__main__":
    main()
