#README file  
Summer 2016, Bitly Data Science Internship- Data Analysis- Chirag Bhupendra Chheda  
Two important aspects:
1.) Folder Structure
2.) Scripts

#Folder Structure  
The folder structure contains three parts:  
Input - Where the raw data file provided is placed  
Data Chunks - Where all the interim data is stored  
Output - Contains beautiful visualisations  

#Scripts  
Script.py - This is the main file with all the data manipulation code  
We perform various functions here such as:  
1.) Data Cleaning - First all the redundant attributes are removed then missing attributes are added to the file in order to make data consistent.  
2.) Data Fragmentation - Since we could not open the whole file, we broke the problem into parts in order to get a better idea of the data.  
3.) Feature Value Counter - This function helps us to obtain statistics about various features.  
4.) Feature Domain Extract - This primarily is used to find out the Domain/Company name and it's popularity among the others.  
5.) Feature Browser OS - This primarily helps us to obtain statistics on the OS, Devices used and Browsers used while accessing bit.ly links.  
6.) Top Level Domain Extraction - Step used to devise links most visited with respect to their User Hash Values.  

#How to Run the code:

Script.py is the file containing all the code.
1.) Just place raw input files into the input folder and create two empty folders in the same directory as the one with the input folder named output and data_chunks.  
2.) Go to script.py and simply manipulate the read_data in the main method. Everything else will run automatically giving you statistics in sorted and unsorted manner.
3.) All interim output will be stored in data_chunks, named appropriately. It is mentioned in step form and all the data manipulations are stored for you to see.

#THANK YOU