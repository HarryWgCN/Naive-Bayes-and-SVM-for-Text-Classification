import os
from jieba import posseg
classes = 10
file_start = 1
file_end = 10000


for ana_class in range(1, classes + 1):  # for each class
    class_dir = f'./data/train_data_ori/{ana_class}'
    for root, dirs, files in os.walk(class_dir):
        # traverse by file object instead of name with order to cope with chaos in naming
        # for ana_file in range(file_start, file_end + 1):  # for each file
        ana_file = 0
        for f in files:
            ana_file += 1
            if ana_file == file_end + 1:
                break
            ori_path = f'./data/train_data_ori/{ana_class}/' + f
            train_file_ori = open(ori_path, 'r', encoding='utf-8')  # the original file to be cut
            train_file_split_path = f'./data/train_data_split/{ana_class}/{ana_file}.txt'  # the file to store result
            split_dir = f'./data/train_data_split/{ana_class}'
            if not os.path.exists(split_dir):
                os.makedirs(split_dir)
            train_file_split = open(train_file_split_path, 'w', encoding='utf-8')
            # cut the file by jieba
            train_data = train_file_ori.read()
            words = posseg.cut(train_data)  # cut the file into words with space(" ")
            for word in words:  # for each word record itself and its flag
                write_str = '{}\t{}\n'.format(str(word.word), str(word.flag))
                write_str.encode('utf-8')
                train_file_split.write(write_str)  # record result in file
            train_file_ori.close()
            train_file_split.close()
