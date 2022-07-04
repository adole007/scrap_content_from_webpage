#EXcel combined
# import libraries
import pandas as pd
import glob
# define folder directory to look in. Change to xlsx if Excel file.
path =r'artwork_content/' 
allFiles = glob.glob(path + "/*.csv")
# make a list of all the files in the folder
list_ = []
for file_ in allFiles:
    # define sheet name and place data starts
    df = pd.read_csv(file_, dtype=str, header=0)
    # create a variable with the filename
    df['filename']= file_
    # extract the date from the filename using string slice
    df['date'] = df['filename'].str[-12:-4]
# stack each file all on top of the other
    list_.append(df)
stack = pd.concat(list_, axis=0)
# output to excel or another database 
stack.to_csv(r'filename.csv')
