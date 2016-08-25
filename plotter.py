# -*- coding: utf-8 -*-
"""
Created on Sun May 15 18:53:14 2016

@author: Chirag Chedda
"""
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import json

def bar_stats(data):
    objects = tuple(data.keys())
    y_pos = np.arange(len(objects))
    performance = list(data.values())
    
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('Web Engines')
    
    plt.show()
    
def pie_stats(data):
    labels = tuple(data.keys())
    sizes = list(data.values())
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    #explode = (0.1, 0, 0, 0)  # explode 1st slice
    
    # Plot
    plt.pie(sizes, labels=labels,
            autopct='%1.1f%%', shadow=True, startangle=140)
            
    plt.axis('equal')
    plt.show()    

def main():
    
    with open('./data_chunks/burrow/1/a-step4-1500-browser.json','rb') as input_file:
        data = json.load(input_file)
    
    bar_stats(data)
    pie_stats(data)
    
if __name__ == "__main__":
    main()