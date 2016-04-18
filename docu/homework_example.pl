#!/usr/bin/perl 

#Part 1
import os
import graphlab
graphlab.product_key.set_product_key('Your API Key')
location = 'http://www.vivekpatani.tk/resources/reuters.csv'
sf = graphlab.SFrame.read_csv(location, header=False)