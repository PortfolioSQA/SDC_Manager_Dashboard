#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 09:19:32 2020

@author: sashaqanderson
"""
import pandas as pd
import random

def load_data(harvest_db, rel_ident):
    #load sample data
    df1 = harvest_db.copy()
    df1.beg_date =  pd.to_datetime(df1.beg_date)
    df1.end_date =  pd.to_datetime(df1.end_date)
    df1.last_update =  pd.to_datetime(df1.last_update)
    df1.last_harvest =  pd.to_datetime(df1.last_harvest)
    df1.index = df1['file_identifier']
    
    df2 = rel_ident.copy()
    # df2 remove is_primary_pub NULL & group by metadata_identifier count is_primary_pub
    df2 = df2[df2['is_primary_pub'].notna()]
    df3 = df2.groupby(["metadata_identifier"]).count()
    df3 = df3[['is_primary_pub']]
    df3.columns = ['citations']
    
    #create a 'status' feature in df1
    size = df1.shape
    inactive_num = int(0.10 * size[0])
    active_num = int(0.90 * size[0])
    my_list = ['Inactive'] * inactive_num + ['Active'] * active_num
    random.shuffle(my_list)
    if size[0] == len(my_list):    
        df1['status'] = my_list
    else:
        my_list = ['Active'] + my_list
        df1['status'] = my_list
        
    #join df1 and citation count
    result = df1.merge(df3, how = 'left', left_index=True, right_index=True)
    result.citations.fillna(0, inplace = True)
    result.datasource.fillna('Unknown', inplace = True)
    result.to_csv('/Users/sashaqanderson/SDC_Manager_Dashboard/final_df.csv', index=False)
    result.columns = ['file_identifier', 'datasource', 'doi', 'beg_date',
       'end_date', 'last_update', 'last_harvest', 'status',
       'citations']
    return result

if __name__ == "__main__":
    df_pub = pd.read_csv('/Users/sashaqanderson/SDC_Manager_Dashboard/related_identifiers_example2.csv')
    df_pub.set_index('metadata_identifier')
    df_sc = pd.read_csv('/Users/sashaqanderson/SDC_Manager_Dashboard/harvest_database_example2.csv')
    df_sc.set_index('file_identifier')
    df = load_data(df_sc, df_pub)
    print(df.columns)
