import os

classes = 10
file_start = 1
file_end = 10000


# to get information about what is in stop_word list
def get_stop_info():
    stop_file = open(f'./data/stop_words_ch.txt', 'r')
    stop_words_in_line = stop_file.readlines()
    stop_words = list()
    for word in stop_words_in_line:
        stop_words.append(word.strip('\n'))
    return stop_words


def main():
    stop_word_list = get_stop_info()  # get stop word information
    for ana_class in range(1, classes + 1):  # for each class
        for ana_file in range(file_start, file_end + 1):  # for each file
            train_aggregate = open(f'./data/train_data_aggregate/{ana_class}/{ana_file}.txt', 'r', encoding='utf-8')
            train_no_stop_path = f'./data/train_data_no_stop/{ana_class}/{ana_file}.txt'
            train_no_stop_dir = f'./data/train_data_no_stop/{ana_class}'
            if not os.path.exists(train_no_stop_dir):
                os.makedirs(train_no_stop_dir)
            train_file_no_stop = open(train_no_stop_path, 'w', encoding='utf-8')
            to_find = train_aggregate.readlines()  # get the line to remove stop_word from
            # remove stop words from file content
            for line in to_find:
                words = line.split(' ')
                for word in words:  # check whether a word is to be reserved
                    if word not in stop_word_list:
                        train_file_no_stop.write(word + ' ')
                train_file_no_stop.write('\n')
            train_aggregate.close()
            train_file_no_stop.close()


main()
