import data_by_player as dbp
import check_processed as cp
import os


def main():
    input_path = './training_data/'
    # output_path = './result_data/'
     
    file_list = os.listdir(input_path)
    print(file_list)

    file_name = input('\nWhat is today training data? :  ')

    file_path = input_path + file_name
    exist_file = os.path.isfile(file_path)
    if exist_file == False:
        print('============================================================================================')
        print('Oooops! file({}) is not exist. Check your directory({}) again.'.format(file_name, input_path))
        print('============================================================================================')
        raise
    cp.check_processed(file_name)
    dbp.result_detail(file_name)


if __name__ == "__main__":
    print('===========================================================')
    print('==                                                       ==')
    print('==        Hi!!! Welcome to physico_PARK world!!!!        ==')
    print('==                                                       ==')
    print('===========================================================')
    main()