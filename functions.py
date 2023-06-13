import numpy as np
import pandas as pd


def av_err(dataset_1, dataset_2, dataset_3):
    """
    function has to work with 1 row at a time, such that it can loop through the data structure and average
    and find error
    """
    
    # we want to make a copy of dataframes, such that we don't work on the originals
    dataset1c = dataset_1.copy()
    dataset2c = dataset_2.copy()
    dataset3c = dataset_3.copy()
    
    # we now create a larger dataframe that contains data from all three runs
    # let's add to the first one and call it a day
    dataset1c['run2'] = dataset2c['counts']
    dataset1c['run3'] = dataset3c['counts']
    
    
    
    # we also want to create an average column and an error column
    dataset1c['average'] = dataset1c[['counts', 'run2', 'run3']].apply(np.average, axis = 1,
                                                                        raw = True, 
                                                                        result_type = 'expand')
#     print(dataset1c.head()) #checkcheck
    dataset1c['error'] = dataset1c.apply(lambda x: np.max(np.abs([x.average - x.counts, x.average - x.run2, x.average - x.run3])),
                                        axis = 1, result_type = 'expand')
    
    return dataset1c[['ADC channel', 'average', 'error']]

def savetocsv(daframe, dipath):
    '''
    dipath should be like "Data/BGO/Am241/BGO_Am241_final.csv"
    '''
    
    daframe.to_csv(dipath)