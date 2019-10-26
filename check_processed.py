import pandas as pd
import os


def check_processed(file_name):
    assistant_path = './assistant_data/'
    assistant_file = 'assistant_data.csv'
    file_path = assistant_path + assistant_file
    exist_file = os.path.isfile(file_path)

    if exist_file:
        assistant_data = pd.read_csv(assistant_path + 'assistant_data.csv')
        if file_name in assistant_data.values:
            print('You already processed {} data.'.format(file_name))
            print('Check file name again!!')
            print("========================================================================================")
            raise
        else:
            adf = pd.DataFrame([file_name], columns=['File_Name'])
            adf.to_csv(assistant_path + 'assistant_data.csv', mode='a', header=False)
    else:
        adf = pd.DataFrame([file_name], columns=['File_Name'])
        adf.to_csv(assistant_path + 'assistant_data.csv')
