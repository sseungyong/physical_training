import pandas as pd
import os


def result_detail(file_name):
    input_path = './training_data/'
    output_path = './result_data/'
     
    # file_list = os.listdir(input_path)
    # print(file_list)

    # file_name = input('What is today training data? : \n')

    file_path = input_path + file_name
    # exist_file = os.path.isfile(file_path)
    # if exist_file == False:
    #     print('============================================================================================')
    #     print('Oooops! file({}) is not exist. Check your directory({}) again.'.format(file_name, input_path))
    #     print('============================================================================================')
    #     raise
    
    xl = pd.ExcelFile(file_path)
    for sn in xl.sheet_names:
        print("========================================================================================")
        print("Training dataset : ", sn, "at", file_path)
        df = xl.parse(sn)
        df['Load'] = df['RPE'] * df['TR_time_(min)']
        info_df = df.loc[0:0, 'Date':'Type']
        mean_df = df.loc[:, 'Height':].mean().to_frame().T
        mean_df = info_df.join(mean_df)

        if os.path.isfile(output_path + 'result_by_player.xlsx'):
            writer = pd.ExcelWriter(output_path + 'result_by_player.xlsx')
            team_df = pd.read_excel(output_path + 'result_by_player.xlsx', sheet_name='Team sheet')

            temp_df = team_df.iloc[:, :-3]
            temp_df = temp_df.append(mean_df, ignore_index=True)

            t_day = len(temp_df)

            if t_day <= 7:
                mean_df['Mono'] = temp_df['Load'].mean() / temp_df['Load'].std()
                mean_df['Strain'] = temp_df['Load'].sum() * mean_df['Mono']
                mean_df['EWAM'] = temp_df['Load'].sum() / temp_df['Load'].sum()
            elif t_day <= 28:
                week_n = t_day - 7
                mean_df['Mono'] = temp_df.loc[week_n:, 'Load'].mean() / temp_df.loc[week_n:, 'Load'].std()
                mean_df['Strain'] = temp_df.loc[week_n:, 'Load'].sum() * mean_df['Mono']
                mean_df['EWAM'] = temp_df.loc[week_n:, 'Load'].sum() / temp_df.loc[week_n:, 'Load'].sum()
            else:
                week_n = t_day - 7
                month_n = t_day - 28
                mean_df['Mono'] = temp_df.loc[week_n:, 'Load'].mean() / temp_df.loc[week_n:, 'Load'].std()
                mean_df['Strain'] = temp_df.loc[week_n:, 'Load'].sum() * mean_df['Mono']
                mean_df['EWAM'] = temp_df.loc[week_n:, 'Load'].sum() / temp_df.loc[month_n:, 'Load'].sum()

            team_df = team_df.append(mean_df, ignore_index=True)
            team_df.to_excel(writer, sheet_name='Team sheet', columns=team_df.columns, index=False, float_format='%.2f')

            for i in range(len(df)):
                player = df.iloc[i].Name
                position = df.iloc[i].Position
                sheet_name = player + '_' + position
                player_data = df.iloc[i:i + 1, 3:]
                player_df = pd.read_excel(output_path + 'result_by_player.xlsx', sheet_name=sheet_name)

                temp_df = player_df.iloc[:, :-3]
                temp_df = temp_df.append(player_data, ignore_index=True)

                t_day = len(temp_df)

                if t_day <= 7:
                    player_data['Mono'] = temp_df['Load'].mean() / temp_df['Load'].std()
                    player_data['Strain'] = temp_df['Load'].sum() * player_data['Mono']
                    player_data['EWAM'] = temp_df['Load'].sum() / temp_df['Load'].sum()
                elif t_day <= 28:
                    week_n = t_day - 7
                    player_data['Mono'] = temp_df.loc[week_n:, 'Load'].mean() / temp_df.loc[week_n:, 'Load'].std()
                    player_data['Strain'] = temp_df.loc[week_n:, 'Load'].sum() * player_data['Mono']
                    player_data['EWAM'] = temp_df.loc[week_n:, 'Load'].sum() / temp_df.loc[week_n:, 'Load'].sum()
                else:
                    week_n = t_day - 7
                    month_n = t_day - 28
                    player_data['Mono'] = temp_df.loc[week_n:, 'Load'].mean() / temp_df.loc[week_n:, 'Load'].std()
                    player_data['Strain'] = temp_df.loc[week_n:, 'Load'].sum() * player_data['Mono']
                    player_data['EWAM'] = temp_df.loc[week_n:, 'Load'].sum() / temp_df.loc[month_n:, 'Load'].sum()

                player_df = player_df.append(player_data, ignore_index=True)
                player_df.to_excel(writer, sheet_name=sheet_name, index=False , float_format='%.2f')

            writer.save()
            
            print("We have result file. Add data on result file")
            print("We workout {} times.".format(t_day))
            print("========================================================================================")

        else:
            writer = pd.ExcelWriter(output_path + 'result_by_player.xlsx')
            mean_df['Mono'] = mean_df['Load'].mean() / mean_df['Load'].std()
            mean_df['Strain'] = mean_df['Load'].sum() * mean_df['Mono']
            mean_df['EWAM'] = mean_df['Load'].sum() / mean_df['Load'].sum()
            mean_df.to_excel(writer, sheet_name='Team sheet', columns=mean_df.columns, index=False, float_format='%.2f')

            for i in range(len(df)):
                player = df.iloc[i].Name
                position = df.iloc[i].Position
                sheet_name = player + '_' + position
                player_data = df.iloc[i:i + 1, 3:]
                player_data['Mono'] = player_data['Load'].mean() / player_data['Load'].std()
                player_data['Strain'] = player_data['Load'].sum() * player_data['Mono']
                player_data['EWAM'] = player_data['Load'].sum() / player_data['Load'].sum()
                player_data.to_excel(writer, sheet_name=sheet_name, columns=player_data.columns, index=False, float_format='%.2f')

            writer.save()

            print("Result file doesn't exist. Make result file")
            print("We workout 1 time")
            print("========================================================================================")

    print("Complete!!!!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")