# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 23:05:37 2016

@author: Vivek Patani
"""

def convert(attr):	
	data={}
	final = []
	i=0
	for each in rows:
		if each in data:continue
		else:
			data[each]=i
			i=i+1

	for  other in rows:
		final.append(data[other])
	return final	
