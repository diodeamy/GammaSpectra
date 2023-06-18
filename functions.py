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
    
def allthewayup(dataset, peakval1, peakval2, peakwidth = 150):
    '''
    I want this function to take the dataset, seek the highest two values of "average", which are the counts;
    and depending on the two peakvalues selected to make the distrinction, to establish the conversion rate;
    from "ADC channel" to energy in electron volts (eVs).
    
    It will have a quirk for the Co60 source, where the identified peaks have to be in a specific region above;
    the 12k channel region (this is clearly where they are by comparing the data obtained with literature)
    '''
    df_sort = dataset.sort_values(by=['average'], 
                              ascending=False, inplace=False)[['ADC channel', 'average', 'error']]
    
    # we first find the largest peak
    dp1 = df_sort.iloc[0]
    print(dp1)
    
    # we then want to remove the peak already found
    dp2 = df_sort[df_sort['ADC channel'] > peakwidth].iloc[0]
    print(dp2)
    
    # now we can find the ratio of conversion
    # i.e. this amount is how many eVs one channel is equivalent to
    ratio = (peakval2 - peakval1)/(dp2['ADC channel'] - dp1['ADC channel'])
    print(ratio)
    
    # all we are left to do now is multiply each channel value by this ratio and BAM!
    datasetc = dataset.copy()
    datasetc['energy'] = datasetc['ADC channel'].apply(lambda x: x*ratio)
        
    return datasetc