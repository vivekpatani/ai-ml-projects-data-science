# -*- coding: utf-8 -*-
"""
Created on Sun May 15 01:02:04 2016

@author: Chirag Chedda
"""
import json
import os
import pickle
import ast
import re
import operator
import time

'''
To read the input file
'''
def read_data(path,filename,ext=""):
    
    #Printing File Location
    print(os.getcwd())
    
    #Printing Path and Filename
    print(path+filename)    
    
    #Actual Data Dictionary
    data_dict = {}
    
    #Dictionary Counter
    count = 0
    
    #Defining Default Dictionary Structure as ID and RECORD
    data_dict.setdefault(count,{})
    
    #Opening Input File
    with open(path+filename,'r') as file_input:
        
        #Walking through each line in file
        for each_line in file_input:
            
            #Adding new records as ID and RECORD
            data_dict[count] = ast.literal_eval(each_line)
            
            #New Record Incrementer
            count += 1
            
            #TEST
#            if count == 1500:
#                break
    
    #To store file as pickle
    with open('./data_chunks/output-500.p','wb') as output_p:
        pickle.dump(data_dict,output_p)
    
    #To store file as JSON
    with open('./data_chunks/output-500.json','w') as output:
        json.dump(data_dict,output,indent=4)
    
    #Clean up
    data_dict.clear()

'''
To clean up the input file
FUNC:
1.) To remove extra attributes
2.) Normalise all attributes
'''
def clean_remove_data(path,filename):
    
    #Defining the basic attribute list for comparison
    attributes = ["h","g","a","u","t","c","nk","kw","ckw","cy","tz"]
    
    #Opening input file to be cleaned
    with open(path+filename,'rb') as input_p:
        data = pickle.load(input_p)
        
    #Temporary List to check each record contents
    tempList = []
    
    #Walking through each record for cleaning
    for each_element in data:
        
        #Storing record in temp list for comparison
        tempList = list(data[each_element].keys())
        
        #Walk through each elemet of tempList for comparison
        for sub_element in tempList:
            
            #Actually compare to see what exists in the list
            #Continue if it exists i.e. Dont care condition
            if sub_element in attributes: continue
            #Remove extra attributes
            else: data[each_element].pop(sub_element, None)
        #Remove the current record
        tempList = []
    
    #To store file as pickle
    with open('./data_chunks/step1-500.json','w') as step1:
        json.dump(data,step1,indent=4,ensure_ascii=False)
        
    #To store file as JSON        
    with open('./data_chunks/step1-500.p','wb') as step1:
        pickle.dump(data,step1)

'''
Function to append missing attributes for records
Helps flatten the data
'''
def clean_add_data(path,filename):
    
    #Defining the basic attribute list for comparison
    attributes = ["h","g","a","u","t","c","nk","kw","ckw","cy","tz"]
    
    #Opening input file to be cleaned
    with open(path+filename,'rb') as input_p:
        data = pickle.load(input_p)
        
    #Temporary List to check each record contents
    tempList = []
    
    #Walking through each record for cleaning
    for each_element in data:
        
        #Storing record in temp list for comparison
        tempList = list(data[each_element].keys())
        
        #Walk through each elemet of tempList for comparison
        for sub_element in attributes:
            
            #Actually compare to see what exists in the list
            #Continue if it exists i.e. Dont care condition
            if sub_element not in tempList:
                data[each_element][sub_element] = None
            #Add extra attributes
            else: continue
        #Remove the current record
        #print(list(data[each_element].keys()))
        tempList = []
    
    #To store file as pickle
    with open('./data_chunks/step2-500.json','w') as step2:
        json.dump(data,step2,indent=4,ensure_ascii=False)
        
    #To store file as JSON        
    with open('./data_chunks/step2-500.p','wb') as step2:
        pickle.dump(data,step2)

'''
Load The Clean File
Testing Function
'''
def load_clean_data(path,file_name,encoding):
    
    print("LOADER")
    with open(path+file_name,'rb') as input_file:
        data = pickle.load(input_file)
    

#'''
#Covert INT to STRING
#'''
#def converter(path,file_name):
#    
#    with open(path+file_name,'rb') as step2:
#        data = pickle.load(step2)
#    
#    for each_element in data:
#        data[each_element]["nk"] = str(data[each_element]["nk"])
#        data[each_element]["t"] = str(data[each_element]["t"])
#    
#    print(path+'step3-500.p')
#    with open(path+'step3-500.p','wb') as step3:
#        pickle.dump(data,step3)
        
#    #To store file as pickle
#    with open(path+'step3-500.json','w') as step3:
#        json.dump(data,step3,indent=4,ensure_ascii=False)
    
#    for each_element in data:
#        for each_sub_element in data[each_element]:
#            #print(type(each_sub_element))

'''
Break file into parts
Helps sample the data
'''
def read_in_chunks(file_name, chunk_size = 1024*1):
    
    #Temp
    count = 0    
    
    #Define the chunk size in multiples of MB
    chunk_size = chunk_size * 50
    
    #Lazy function (generator) to read a file piece by piece. Default chunk size: 1k.
    while True:

        data = file_name.read(chunk_size)

        #If it's the end then break
        if not data:
            break

        else:
            yield(data)
            count += 1
            if count == 2:
                break

'''
Generates a JSON File consisting of Feature:Value pair
Works for
1.) Feature H
2.) Feature C
3.) Feature CY
4.) Feature TZ
'''
def feature_value_counter(path,file_name,feature):
    
    #Will store all the possible duplicate feature values
    feature_value = []
    
    #Open the file generated in step 3
    with open(path+file_name,'rb') as step3:
        data = pickle.load(step3)
    
    #Walk through each record in the dictionary
    for each_element in data:
        feature_value.append(data[each_element][feature])
    
    #Find out unique Features
    feature_unique = {}
    
    #Walk through each element
    for each_element in data:
        
        #Incrementing the count for already existant features
        if data[each_element][feature] in feature_unique:
            feature_unique[data[each_element][feature]] += 1
            
        #Initialising Count for non existant feature
        else: feature_unique[data[each_element][feature]] = 1
    
    #Sorted to understand, data better
    sorted_x = sorted(feature_unique.items(), key=operator.itemgetter(1),reverse=True)
    
    #To store file as pickle
    with open(path+feature+'-step4-500.json','w') as step4:
        json.dump(feature_unique,step4,indent=4,ensure_ascii=False)
    
    #To store file as pickle
    with open(path+feature+'-step4-500.p','w') as step4:
        json.dump(feature_unique,step4)
    
    #To store SORTED objects
    with open(path+feature+'-step4-500-sorted.json','w') as step4:
        json.dump(sorted_x,step4,indent=4,ensure_ascii=False)

'''
Finding the Domain of each decode
'''
def feature_domain_extract(path,file_name):
    
    #Extracting domain/company names
    domain_counter = {}
    counterwa = 0
    
    with open(path+file_name,'rb') as step3:
        data = pickle.load(step3)
    
    for each_item in data:
        counterwa += 1
        print(counterwa)
        try:
            current = data[each_item]["u"].lower()
            link = re.search('//(.*)/',current)
            sub_link = link.group(1).split('/')
            #print(sub_link[0])
            current = sub_link[0].split(".")
            if len(current) <= 2:
                if current[0] in domain_counter:
                    #print(current[0])
                    domain_counter[current[0]] += 1
                else: domain_counter[current[0]] = 1
            else:
                if current[1] in domain_counter:
                    domain_counter[current[1]] += 1
                else: domain_counter[current[1]] = 1
        
        except Exception:
            print("Error"+str(counterwa))
    
    sorted_x = sorted(domain_counter.items(), key=operator.itemgetter(1),reverse=True)
    
    #UNSORTED DICT
    with open(path+"u"+'-step4-1500-dom.json','w') as step4:
        json.dump(domain_counter,step4,indent=4,ensure_ascii=False)
    
    with open(path+"u"+'-step4-1500-dom.p','wb') as step4:
        pickle.dump(domain_counter,step4)
    
    with open(path+"u"+'-step4-1500-sorted-dom.json','w') as step4:
        json.dump(sorted_x,step4,indent=4,ensure_ascii=False)

'''
Returns The Count of Each Web Engine Used
'''
def feature_browser_os_counter(path,file_name):
    
    browser_list = ["chrome","msie","firefox","safari","maxthon","opera","netscape","avant","ucbrowser"]
    os_list = ["windows","linux","mac","compatible"]
    device_list = ["android","iphone"]
    
    browser_counter = {}
    os_counter = {}
    device_counter = {}
    
    with open(path+file_name,'rb') as step3:
        data = pickle.load(step3)
          
    for each_item in data:
        current = data[each_item]["a"].lower()
        for each_browser in browser_list:
            if each_browser not in browser_counter:
                browser_counter[each_browser] = 0
            if re.search(each_browser,current):
                #print(each_browser)
                browser_counter[each_browser] += 1
                break

        for each_os in os_list:
            if each_os not in os_counter:
                os_counter[each_os] = 0
            if re.search(each_os,current):
                #print(each_os)
                os_counter[each_os] += 1
                break
        
        for each_device in device_list:
            if each_device not in device_counter:
                device_counter[each_device] = 0
            if re.search(each_device,current):
                #print(each_device)
                device_counter[each_device] += 1
                break
        
    sorted_x = sorted(browser_counter.items(), key=operator.itemgetter(1),reverse=True)
    sorted_y = sorted(os_counter.items(), key=operator.itemgetter(1),reverse=True)
    sorted_z = sorted(device_counter.items(), key=operator.itemgetter(1),reverse=True)
    
    with open(path+"a"+'-step4-1500-browser.json','w') as step4:
        json.dump(browser_counter,step4,indent=4,ensure_ascii=False)
                
    with open(path+"a"+'-step4-1500-os.json','w') as step4:
        json.dump(os_counter,step4,indent=4,ensure_ascii=False)
    
    with open(path+"a"+'-step4-1500-device.json','w') as step4:
        json.dump(device_counter,step4,indent=4,ensure_ascii=False)
        
    with open(path+"a"+'-step4-1500-browser-sorted.json','w') as step4:
        json.dump(sorted_x,step4,indent=4,ensure_ascii=False)
                
    with open(path+"a"+'-step4-1500-os-sorted.json','w') as step4:
        json.dump(sorted_y,step4,indent=4,ensure_ascii=False)
    
    with open(path+"a"+'-step4-1500-device-sorted.json','w') as step4:
        json.dump(sorted_z,step4,indent=4,ensure_ascii=False)

def tld(data,path,file_name):
    
    count = 0
    usr_hash = []    
    for each_item in data:
        usr_hash.append(each_item)
        count+=1
        if count == 10: break
        
    with open(path+file_name,'rb') as step2:
        input_file = pickle.load(step2)
    
    for each_item in input_file:
        print(each_item)
        for each_hash in usr_hash:
            #print(each_hash)
            if each_hash[0] == input_file[each_item]["h"]:
                each_hash[0] = input_file[each_item]["u"]
    
    #print(usr_hash)
    
    with open(path+'step5-links.json','w') as output_file:
        json.dump(usr_hash,output_file,indent=4,ensure_ascii=False)
'''
Driver Function
'''         
def main():
    start = time.time()
    print(start)
    print("Read")
    read_data('./input/','decodes03')
    
    print("Clean 1")    
    clean_remove_data('./data_chunks/','output-500.p')
    
    print("Clean 2")    
    clean_add_data('./data_chunks/','step1-500.p')
    
    print("Final")    
    load_clean_data('./data_chunks/','step2-500.p',"iso-8859-1")
        
    print("CY")
    feature_value_counter('./data_chunks/','step2-500.p','cy')
    
    print("H")    
    feature_value_counter('./data_chunks/','step2-500.p','h')
    
    print("C")    
    feature_value_counter('./data_chunks/','step2-500.p','c')
    
    print("TZ")    
    feature_value_counter('./data_chunks/','step2-500.p','tz')
    
    print("OS")    
    feature_browser_os_counter('./data_chunks/','step2-500.p')
    
    print("DOMAIN")    
    feature_domain_extract('./data_chunks/','step2-500.p')
    
    #Extract TLD
    with open('./data_chunks/h-step4-500-sorted.json') as input_file:
        data = json.load(input_file)
    tld(data,'./data_chunks/','step2-500.p')
    
    end = time.time()
    
    print((end-start)/60)
    
'''
Standard Boilerplate
'''
if __name__ == "__main__":
    main()