# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 17:42:50 2016

@author: Vivek Patani
"""

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    data_dump = ""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            print(data_dump)
            break
        else:
            line = data.readline()
            return line
            


f = open("./enwikiquote-20160203-pages-articles-multistream.xml/enwikiquote-20160203-pages-articles-multistream.xml")
counter = 0
for piece in read_in_chunks(f):
    print(piece)
    