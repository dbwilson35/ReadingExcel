#import the libraries
import pandas as pd
import os
import datetime
import re
import numpy as np

location = ''

list_of_files = os.listdir(location)

#some functions I need
# get the F1221 from the file name
def get_type(x):
    if x.split()[0] == 'Test':
        return 'S1'
    elif x.split()[0] == 'Not':
        return 'S2'
    elif x.split()[0] == 'Real':
        return 'S3'
    else:
        return 'S4'


# get the date of the report from the file name
# and turn it into a date
def get_date(x):
    date = re.findall('\d\d.\d\d.\d\d\d\d', x)[0]
    date = datetime.datetime.strptime(date, '%m.%d.%Y')
    return date


#to get the months between!
def months_between(d1, d2):
    return (d2.year - d1.year)*12 + d2.month - d1.month

#blank dictionary to fill with results from the loop
blank_dict = {}

for file in list_of_files:
    #create a dictionary of the file
    dict = pd.read_excel(location + '/' + file , sheet_name=['Sheet1'])

    #create a dataframe of the file.
    df = pd.concat(dict[frame] for frame in dict.keys())

    #rename some columns
    df = df.rename(columns={'Column 1': 'Name',
                            'Date': 'New Date',
                            })
    #Only grab the columns I want.
    # I don't know which columns are going to be on things, but i do know which columns i want, so i'm just going to grab thoseones
    df = df[['Name',
             'New Date',
             'Volume',
             'A Volume',
             'No S Volume',
             'S Volume',
             'S % of All',
             'P S Volume',
             'P S %',
             'J Volume',
             'J % Volume',
             'Peas',
             'Peas %'
             ]]
    #add some columns
    df['type'] = get_type(file)
    df['File Date'] = get_date(file)

    #remove blank rows
    df['No S Volume'].replace('',np.nan, inplace=True)
    df.dropna(subset = ['No S Volume'], inplace = True)

    blank_dict[get_type(file) + str(get_date(file))] = df

df_final = pd.concat(blank_dict[frame] for frame in blank_dict.keys())

df_final['Name'] = [x[:4] for x in df_final['Name']]
df_final['Batch'] = [months_between(df_final.loc[x,'New Date'],df_final.loc[x, 'File Date']) for x in range(len(df_final.axes[0]))]

df_final.to_csv('output.csv')



