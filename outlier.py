from __future__ import print_function
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 02:46:51 2016

@author: Chirag Chheda
"""
from pprint import pprint
import script

'''
This method returns the outliers of each attribute through Quantile calculation
'''
def outlier(path,file_name,encoding="iso-8859-1"):
    
    #Dictionary to store data
    data_dict = {}
    
    #Simply Loading Data
    dataset = script.data_loader(path,file_name)
    
    #List of feature for which you'd like to find outliers for
    feature_list = ["id","member_id","loan_amnt","funded_amnt","funded_amnt_inv","term","int_rate","installment","grade","sub_grade","emp_title","emp_length","home_ownership","annual_inc","verification_status","issue_d","pymnt_plan","url","purpose","title","zip_code","addr_state","dti","delinq_2yrs","earliest_cr_line","inq_last_6mths","mths_since_last_delinq","mths_since_last_record","open_acc","pub_rec","revol_bal","revol_util","total_acc","initial_list_status","out_prncp","out_prncp_inv","total_pymnt","total_pymnt_inv","total_rec_prncp","total_rec_int","total_rec_late_fee","recoveries","collection_recovery_fee","last_pymnt_d","last_pymnt_amnt","next_pymnt_d","last_credit_pull_d","collections_12_mths_ex_med","mths_since_last_major_derog","policy_code","application_type","acc_now_delinq","tot_coll_amt","tot_cur_bal","total_rev_hi_lim","acc_open_past_24mths","avg_cur_bal","bc_open_to_buy","bc_util","chargeoff_within_12_mths","delinq_amnt","mo_sin_old_il_acct","mo_sin_old_rev_tl_op","mo_sin_rcnt_rev_tl_op","mo_sin_rcnt_tl","mort_acc","mths_since_recent_bc","mths_since_recent_bc_dlq","mths_since_recent_inq","mths_since_recent_revol_delinq","num_accts_ever_120_pd","num_actv_bc_tl","num_actv_rev_tl","num_bc_sats","num_bc_tl","num_il_tl","num_op_rev_tl","num_rev_accts","num_rev_tl_bal_gt_0","num_sats","num_tl_120dpd_2m","num_tl_30dpd","num_tl_90g_dpd_24m","num_tl_op_past_12m","pct_tl_nvr_dlq","percent_bc_gt_75","pub_rec_bankruptcies","tax_liens","tot_hi_cred_lim","total_bal_ex_mort","total_bc_limit","total_il_high_credit_limit"]
    
    #Open a stream to output files
    outfile = open('./output/output.txt','a')
    
    #For each feature in the feature list
    for each_feature in feature_list:
        #If the feature is categorical
        if dataset[each_feature].dtype == "object":
            print(end = "")
        else:
            #Else if it is an int64 or float64
            #Finding Quantiles for detection of Outliers
            q3 = dataset[each_feature].quantile(q=0.75)
            q1 = dataset[each_feature].quantile(q=0.25)
            iqr = q3 - q1
            
            #Calculating upper and lower bounds
            lb = (q1 - iqr * 1.5)
            ub = (q3 + iqr * 1.5)

            data_dict.setdefault(each_feature,[])
            data_list = []
            
            #Walk through each row of the current feature            
            for each_row in range(len(dataset.loc[:,each_feature])):
                
                #Let us select a current record
                current = dataset.loc[each_row,each_feature]
                
                #If it lies beyond these bounds then it is an outlier
                if current < lb or current > ub:
                    data_list.append(current)
            
            #If the list is empty do not bother adding it
            if len(data_list):
                data_dict[each_feature] = data_list
                    
    pprint(data_dict,stream=outfile)
    
    #Close the file
    outfile.close()
    
def main():
    
    #Call the outlier method
    outlier('./input/','lc2015.csv')
#    outlier('./input/','test.csv')

'''
Boilerplate
'''
if __name__ == "__main__":
    main()