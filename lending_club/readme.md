#Chriag Chheda - Lending Club Analysis

#What the Script Does?  
This Script(script.py) is used to find the best predictors for the class variable 'Loan Status' in the Lending Club Data.  

The Outlier(outlier.py) script is used to detect outliers for each of the features in the dataset.  

#How to run it?  
##Maintain the Foler Structure:  
Make three folders in the root directory of the project namely:  
1.) input  
2.) output  
3.) data_chunks  

Then place outlier.py and script.py in the root directory.  

Place raw data in the input file and change the name accordingly in the main call in script.py and outlier.py.  

Need sklearn libraries.  

Everything else will work fine.

#Output
##For The Best Features:
Alpha = 0.00  
['total_rec_late_fee','total_rec_int','last_pymnt_amnt','recoveries','acc_open_past_24mths']  
Coefficients:  
 [  1.42198429e-03  -6.71579809e-06   3.04515661e-05  -1.67330796e-03
   2.28599690e-02]  
Residual sum of squares: 0.59  
Variance score: 0.23  
  
Alpha = 0.001  
['last_pymnt_amnt','out_prncp','total_rec_late_fee','recoveries','int_rate','collection_recovery_fee']  
Coefficients:  
 [  2.70101739e-05  -7.82766166e-06   1.35738392e-03  -8.44078455e-04
   3.44427218e-03  -1.08504724e-03]  
Residual sum of squares: 0.55  
Variance score: 0.28  

##For Outliers:
The report covers it, outlier output is located in output folder as output.txt after running the script

#Thank you for the opportunity