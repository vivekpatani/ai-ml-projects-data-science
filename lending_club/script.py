# -*- coding: utf-8 -*-
"""
Created on Tue May 17 20:27:43 2016

@author: Chirag Chheda
"""
from sklearn import preprocessing as p
from sklearn.base import TransformerMixin
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import RandomizedLasso
import json


'''
This is a Data Frame Cleaner
Assigns "mean" values to the missing values
KIM: There should be atleast one value in the attribute list else eliminate the attribute
'''
class DataFrameImputer(TransformerMixin):

    def __init__(self):
        """Impute missing values.

        Columns of dtype object are imputed with the most frequent value 
        in column.

        Columns of other types are imputed with mean of column.

        """
    def fit(self, X, y=None):

        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns)

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)

'''
Returns data frame (Pandas) when given a CSV Input
'''
def data_loader(path,file_name,encoding='iso-8859-1'):
    
    #To actually open the stream for a CSV File
    with open(path+file_name) as input_file:
        data = pd.read_csv(input_file)
    return data

'''
Performs various functions:
1.) Transforms Categorical Attributes to Numerical Attributes
2.) Implements Randomised Lasso to determine the best attributes applying a small penalty
3.) Implements Logistic Regression to see how accurate our IV's are to determine the prediction of loan status
'''
def data_analyse(path,file_name):
    
    #This is used to load the dataset
    dataset = data_loader(path,file_name)
    
    #Clean up the dataset by assigning mean
    dataset = DataFrameImputer().fit_transform(dataset)
    
    #Our Class/Prediction Variable
    Y = dataset['loan_status']
    
    '''
    1.) Transformations
    '''    
    
    #Transforming the Class Variable
    le = p.LabelEncoder()
    le.fit(Y)
    tr = le.transform(Y)
    
    #Penaly Application Variable for the lasso model
    alpha = 0.001
    
    #Just to keep a count on if any exceptions occur
    count = 0
    
    #Used as Attribute list from which we will select the best predictors for our Class Variable
    X = dataset[["id","member_id","loan_amnt","funded_amnt","funded_amnt_inv","term","int_rate","installment","grade","sub_grade","emp_title","emp_length","home_ownership","annual_inc","verification_status","issue_d","pymnt_plan","url","purpose","title","zip_code","addr_state","dti","delinq_2yrs","earliest_cr_line","inq_last_6mths","mths_since_last_delinq","mths_since_last_record","open_acc","pub_rec","revol_bal","revol_util","total_acc","initial_list_status","out_prncp","out_prncp_inv","total_pymnt","total_pymnt_inv","total_rec_prncp","total_rec_int","total_rec_late_fee","recoveries","collection_recovery_fee","last_pymnt_d","last_pymnt_amnt","next_pymnt_d","last_credit_pull_d","collections_12_mths_ex_med","mths_since_last_major_derog","policy_code","application_type","acc_now_delinq","tot_coll_amt","tot_cur_bal","total_rev_hi_lim","acc_open_past_24mths","avg_cur_bal","bc_open_to_buy","bc_util","chargeoff_within_12_mths","delinq_amnt","mo_sin_old_il_acct","mo_sin_old_rev_tl_op","mo_sin_rcnt_rev_tl_op","mo_sin_rcnt_tl","mort_acc","mths_since_recent_bc","mths_since_recent_bc_dlq","mths_since_recent_inq","mths_since_recent_revol_delinq","num_accts_ever_120_pd","num_actv_bc_tl","num_actv_rev_tl","num_bc_sats","num_bc_tl","num_il_tl","num_op_rev_tl","num_rev_accts","num_rev_tl_bal_gt_0","num_sats","num_tl_120dpd_2m","num_tl_30dpd","num_tl_90g_dpd_24m","num_tl_op_past_12m","pct_tl_nvr_dlq","percent_bc_gt_75","pub_rec_bankruptcies","tax_liens","tot_hi_cred_lim","total_bal_ex_mort","total_bc_limit","total_il_high_credit_limit"]]
    
    #Just to display the score and values of each attribute    
    names = ["id","member_id","loan_amnt","funded_amnt","funded_amnt_inv","term","int_rate","installment","grade","sub_grade","emp_title","emp_length","home_ownership","annual_inc","verification_status","issue_d","pymnt_plan","url","purpose","title","zip_code","addr_state","dti","delinq_2yrs","earliest_cr_line","inq_last_6mths","mths_since_last_delinq","mths_since_last_record","open_acc","pub_rec","revol_bal","revol_util","total_acc","initial_list_status","out_prncp","out_prncp_inv","total_pymnt","total_pymnt_inv","total_rec_prncp","total_rec_int","total_rec_late_fee","recoveries","collection_recovery_fee","last_pymnt_d","last_pymnt_amnt","next_pymnt_d","last_credit_pull_d","collections_12_mths_ex_med","mths_since_last_major_derog","policy_code","application_type","acc_now_delinq","tot_coll_amt","tot_cur_bal","total_rev_hi_lim","acc_open_past_24mths","avg_cur_bal","bc_open_to_buy","bc_util","chargeoff_within_12_mths","delinq_amnt","mo_sin_old_il_acct","mo_sin_old_rev_tl_op","mo_sin_rcnt_rev_tl_op","mo_sin_rcnt_tl","mort_acc","mths_since_recent_bc","mths_since_recent_bc_dlq","mths_since_recent_inq","mths_since_recent_revol_delinq","num_accts_ever_120_pd","num_actv_bc_tl","num_actv_rev_tl","num_bc_sats","num_bc_tl","num_il_tl","num_op_rev_tl","num_rev_accts","num_rev_tl_bal_gt_0","num_sats","num_tl_120dpd_2m","num_tl_30dpd","num_tl_90g_dpd_24m","num_tl_op_past_12m","pct_tl_nvr_dlq","percent_bc_gt_75","pub_rec_bankruptcies","tax_liens","tot_hi_cred_lim","total_bal_ex_mort","total_bc_limit","total_il_high_credit_limit"]
    
    #Walk through each attribute
    for x in X:
        try:
            #Transformation of Categorical Variable
            le = p.LabelEncoder()
            le.fit(dataset[x])
            dataset[x] = le.transform(dataset[x])
        except Exception:
            #If there are no values
            count += 1
    
    #Just Refreshing X after transformation
    X = dataset[["id","member_id","loan_amnt","funded_amnt","funded_amnt_inv","term","int_rate","installment","grade","sub_grade","emp_title","emp_length","home_ownership","annual_inc","verification_status","issue_d","pymnt_plan","url","purpose","title","zip_code","addr_state","dti","delinq_2yrs","earliest_cr_line","inq_last_6mths","mths_since_last_delinq","mths_since_last_record","open_acc","pub_rec","revol_bal","revol_util","total_acc","initial_list_status","out_prncp","out_prncp_inv","total_pymnt","total_pymnt_inv","total_rec_prncp","total_rec_int","total_rec_late_fee","recoveries","collection_recovery_fee","last_pymnt_d","last_pymnt_amnt","next_pymnt_d","last_credit_pull_d","collections_12_mths_ex_med","mths_since_last_major_derog","policy_code","application_type","acc_now_delinq","tot_coll_amt","tot_cur_bal","total_rev_hi_lim","acc_open_past_24mths","avg_cur_bal","bc_open_to_buy","bc_util","chargeoff_within_12_mths","delinq_amnt","mo_sin_old_il_acct","mo_sin_old_rev_tl_op","mo_sin_rcnt_rev_tl_op","mo_sin_rcnt_tl","mort_acc","mths_since_recent_bc","mths_since_recent_bc_dlq","mths_since_recent_inq","mths_since_recent_revol_delinq","num_accts_ever_120_pd","num_actv_bc_tl","num_actv_rev_tl","num_bc_sats","num_bc_tl","num_il_tl","num_op_rev_tl","num_rev_accts","num_rev_tl_bal_gt_0","num_sats","num_tl_120dpd_2m","num_tl_30dpd","num_tl_90g_dpd_24m","num_tl_op_past_12m","pct_tl_nvr_dlq","percent_bc_gt_75","pub_rec_bankruptcies","tax_liens","tot_hi_cred_lim","total_bal_ex_mort","total_bc_limit","total_il_high_credit_limit"]]
    
    '''
    2.) Lasso Implementation
    '''
    rlasso = RandomizedLasso(alpha=alpha)
    rlasso.fit(X, tr)
    
    #To sort the attributes according to the Lasso Suggested Score
    output = (sorted(zip(map(lambda x: round(x, 4), rlasso.scores_), 
                 names), reverse=True))
    
    #Just to tag the alpha related to the output, so that keeping track is easy
    output.insert(0,[alpha,"Alpha:"])
    
    #Writing the output to a file for further reference.
    with open('./output/d_analysis-'+str(alpha)+'-.json','w') as output_file:
        json.dump(output,output_file,indent=4,ensure_ascii=False)
        
    '''
    3.) Linear Regression Model
    '''
    
    #Selecting the output from Lasso and selecting variables with high scores
    dataset = dataset[['total_rec_late_fee','total_rec_int','last_pymnt_amnt','recoveries','acc_open_past_24mths','last_pymnt_d']]
    
    #Splitting the train data into parts        
    len_train = int(len(dataset.index)*0.75) * (-1)
    X_train = dataset[:len_train]
    Y_train = tr[:len_train]
    
    #Splitting the data into test
    len_test = int(len(dataset.index)*0.25) * (-1)
    X_test = dataset[len_test:]
    Y_test = tr[len_test:]
    
    # Create linear regression object
    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)
    
    #Just to see how algorithm performed
    print('Coefficients: \n', regr.coef_)
    
    #R2 score
    print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(X_test) - Y_test) ** 2))
     
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(X_test, Y_test))

    
def main():
    
    #Analyse data call
#    data_analyse('./input/','lc2015.csv')
    
    #Only for testing
    data_analyse('./input/','test.csv')

'''
Standard Boilerplate
'''
if __name__ == "__main__":
    main()