#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 09:19:32 2020

@author: sashaqanderson
"""
import pandas as pd
# import numpy as np
import random


def load_data(harvest_db, rel_ident):
    #load sample data
    df1 = harvest_db.copy()
    df1['first_harvest_date'] =  pd.to_datetime(df1['first_harvest_date'])
    df1['last_harvest_date'] =  pd.to_datetime(df1['last_harvest_date'])
    df1['last_mdate_check_date'] =  pd.to_datetime(df1['last_mdate_check_date'])
    df1['mdate'] =  pd.to_datetime(df1['mdate'])
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
    my_list = [0] * inactive_num + [1] * active_num
    random.shuffle(my_list)
    if size[0] == len(my_list):    
        df1['status'] = my_list
    else:
        my_list = [1] + my_list
        df1['status'] = my_list
        
    #join df1 and citation count
    result = df1.merge(df3, how = 'left', left_index=True, right_index=True)
    result.citations.fillna(0, inplace = True)
    result.datasource.fillna('Unknown', inplace = True)

    
    return result

