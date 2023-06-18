import numpy as np
import pandas as pd


def av_err(dataset_1, dataset_2, dataset_3):
    """
    description bla bla
    
    """
    
    # we want to make a copy of dataframes, such that we don't work on the originals
    dataset1c = dataset_1.copy()
    dataset2c = dataset_2.copy()
    dataset3c = dataset_3.copy()
    
    # we now create a larger dataframe that contains data from all three runs
    # let's add to the first one and call it a day
    dataset1c['run2'] = dataset2c['counts']
    dataset1c['run3'] = dataset3c['counts']
    
    print(dataset1c.head())
    
    # we also want to create an average column and an error column
    dataset1c['average'] = dataset1c[['counts', 'run2', 'run3']].apply(np.average, axis = 1,
                                                                        raw = True, 
                                                                        result_type = 'expand')
#     print(dataset1c.head()) #checkcheck
    dataset1c['error'] = dataset1c.apply(lambda x: np.max(np.abs([x.average - x.counts, x.average - x.run2, x.average - x.run3])),
                                        axis = 1, result_type = 'expand')
    print(dataset1c.head())
    return dataset1c[['ADC channel', 'average', 'error']]

def savetocsv(daframe, dipath):
    '''
    dipath should be like "Data/BGO/Am241/BGO_Am241_final.csv"
    '''
    
    daframe.to_csv(dipath)
    
def allthewayup(dataset, peak1, peak2, islarger, peakwidth = 150, iscobalt = 0):
    '''
    I want this function to take the dataset, seek the highest two values of "average", which are the counts;
    it will then return a dictionary object linking the energy and bins at each peak for later consumption
    
    Params
    -------
    dataset: the data to be processed
    peak1: the literature value for where the highest peak should be
    peak2: the literature value for where the second highest peak should be
    islarger: 0 if the second-highest peak is at a higher energy level than the first
              1 if the second-highest peak is at a lower energy level than the first
    peakwidth: approximate peak width(will be removed from dataset in order to find the second peak)
    iscobalt: the cobalt sample was being very difficult; we need to look in the >12k bin range for it
              put 1 for this if you are assessing cobalt
    
    
    Returns
    -------
    dictionary object
    
    '''
    df_sort = dataset.sort_values(by=['average'], 
                              ascending=False, inplace=False)[['ADC channel']]
    if iscobalt == 1:
        dp1 = df_sort[df_sort['ADC channel']> 12000].iloc[0]
        
        dp2 = df_sort[df_sort['ADC channel'] > peakwidth+12000].iloc[0]
    
    elif iscobalt == 0:
        
        dp1 = df_sort.iloc[0]
    
        if islarger == 0:
            dp2 = df_sort[df_sort['ADC channel'] > peakwidth].iloc[0]
        
        elif islarger == 1:
            dp2 = df_sort[df_sort['ADC channel'] < peakwidth].iloc[0]
    
    my_dict = {'peak1': {'energy': peak1, 'channel':dp1[0]}, 'peak2':{'energy': peak2, 'channel':dp2[0]}}
    
    
    return my_dict
