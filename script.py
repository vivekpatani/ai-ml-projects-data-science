"""
Created on Fri Mar 04 17:42:50 2016
@author: Vivek Patani
"""
import os
import sys

#The function to acquire the first x chunk size
def read_in_chunks(file_object, chunk_size=1024):

    #Define the chunk size in multiples of KB
    chunk_size = chunk_size * 50
    
    #Lazy function (generator) to read a file piece by piece. Default chunk size: 1k.
    while True:

        data = file_object.read(chunk_size)

        #If it's the end then break
        if not data:
            break

        else:
            yield(data)
            
def data_gen(path,filename):
    #To get the current working directory.
    print(os.getcwd())

    #File opening Command
    f = open("enwikiquote-20160203-pages-articles-multistream.xml/enwikiquote-20160203-pages-articles-multistream.xml",encoding="iso-8859-1")

    #Process to break the read file and store it in chunks
    counter = 0
    for piece in read_in_chunks(f):
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
        if(counter == 1):
            break
