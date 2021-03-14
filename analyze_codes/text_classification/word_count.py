import os
import math

overall_count_dict = dict()
a_dict = dict()
appearance_dict = dict()  # for recording the number of files this word appears in
classes = 10
train_file_start = 1
train_file_end = 5000
test_file_start = 5001
test_file_end = 10000


def count(ana_class, line):
    global overall_count_dict
    global appearance_dict
    count_dict = dict()
    line_split = line.split(' ')
    for word in line_split:
        if word == '\n':
            continue
        if word in count_dict:
            count_dict[str(word)] += 1  # initialize a record for this word
        else:
            count_dict[str(word)] = 1  # add one count for this word
        if word in overall_count_dict[ana_class]:
            overall_count_dict[ana_class][word] += 1
        else:
            overall_count_dict[ana_class][word] = 1
    for word, value in count_dict.items():
        if word in appearance_dict:
            appearance_dict[word] += 1
        else:
            appearance_dict[word] = 1
    return count_dict


def get_b_from_a(a):
    B = {}
    for file_class in a:
        B[file_class] = {}
        for word in a[file_class]:
            B[file_class][word] = 0
            for other_class in a:
                if other_class != file_class and word in a[other_class]:
                    B[file_class][word] += a[other_class][word]
    return B


def feature_select_use_new_CHI(A, B):
    # CHI method: chi = N*（AD-BC）^2/((A+C)*(B+D)*(A+B)*(C+D)) while N,(A+C),(B+D) be constants(omitted)
    word_features = dict()
    N = 50000
    for ana_class in range(1, classes + 1):
        word_features[ana_class] = list()
        CHI = dict()
        # M = N - 5000
        for word in A[ana_class]:
            temp = pow((A[ana_class][word] * (5000 - B[ana_class][word]) - (5000 - A[ana_class][word]) *
                        B[ana_class][word]), 2) / ((A[ana_class][word] + B[ana_class][word]) *
                                                   (N - A[ana_class][word] - B[ana_class][word]))
            CHI[word] = math.log(N / (A[ana_class][word] + B[ana_class][word]), 2) * temp
        # select the most appearing 400 words as feature
        a = sorted(CHI.items(), key=lambda t: t[1], reverse=True)
        if len(a) > 400:
            a = a[:400]
        for word in a:
            if word not in word_features:
                word_features[ana_class].append(word)
    return word_features


def train_main():
    global overall_count_dict
    global appearance_dict
    global a_dict
    for ana_class in range(1, classes + 1):
        overall_count_dict[ana_class] = dict()
        word_count_dir = f'./data/train_data_word_count/{ana_class}'
        if not os.path.exists(word_count_dir):
            os.makedirs(word_count_dir)
        for ana_file in range(train_file_start, train_file_end + 1):
            train_file_no_stop = open(f'./data/train_data_no_stop/{ana_class}/{ana_file}.txt', 'r', encoding='utf-8')
            # word_count_file_path = f'./data/train_data_word_count_new/{ana_class}/{ana_file}.txt'
            # train_file_word_count = open(word_count_file_path, 'w')
            words = train_file_no_stop.read()
            now_file_count = count(ana_class, words)
            sorted_dict = sorted(now_file_count.items(), key=lambda d: d[1], reverse=True)
            for temp_dict in sorted_dict:
                if temp_dict[0] == ' ':
                    continue
                # write_str = str(temp_dict[0]) + ' ' + str(temp_dict[1]) + '\n'
                # train_file_word_count.write(write_str)
            train_file_no_stop.close()
            # train_file_word_count.close()
        a_dict[ana_class] = appearance_dict
        appearance_dict = dict()

    b_dict = get_b_from_a(a_dict)
    new_feature_dict = feature_select_use_new_CHI(a_dict, b_dict)

    if not os.path.exists('./data/train_data_word_count_new'):
        os.makedirs('./data/train_data_word_count_new')
    for ana_class in range(1, classes + 1):
        train_file_word_count_overall = open(f'./data/train_data_word_count_new/{ana_class}.txt', 'w', encoding='utf-8')
        # calculate the sum of word_count i  one class
        count_sum = 0
        for word, value in overall_count_dict[ana_class].items():
            count_sum += value
        # sort the dict in descending order
        # sorted_dict = sorted(overall_count_dict[ana_class].items(), key=lambda d: d[1], reverse=True)
        train_file_word_count_overall.write(str(count_sum) + '\n')
        for word in new_feature_dict[ana_class]:
            value = overall_count_dict[ana_class][word[0]]
            if word == ' ':
                continue
            write_str = str(word[0]) + ' ' + str(int(value)) + '\n'
            train_file_word_count_overall.write(write_str)
        train_file_word_count_overall.close()


def test_main():
    for ana_class in range(1, classes + 1):
        global overall_count_dict
        overall_count_dict[ana_class] = dict()
        word_count_dir = f'./data/train_data_word_count_test/{ana_class}'
        if not os.path.exists(word_count_dir):
            os.makedirs(word_count_dir)
        train_file_word_count_overall = open(f'./data/train_data_word_count_test/{ana_class}.txt', 'w',
                                             encoding='utf-8')
        for ana_file in range(test_file_start, test_file_end + 1):
            train_file_no_stop = open(f'./data/train_data_no_stop/{ana_class}/{ana_file}.txt', 'r', encoding='utf-8')
            # word_count_file_path = f'./data/train_data_word_count_test/{ana_class}/{ana_file}.txt'
            # train_file_word_count = open(word_count_file_path, 'w')
            words = train_file_no_stop.read()
            now_file_count = count(ana_class, words)
            sorted_dict = sorted(now_file_count.items(), key=lambda d: d[1], reverse=True)
            for temp_dict in sorted_dict:
                if temp_dict[0] == ' ':
                    continue
                # write_str = str(temp_dict[0]) + ' ' + str(temp_dict[1]) + '\n'
                # train_file_word_count.write(write_str)
            train_file_no_stop.close()
            # train_file_word_count.close()
        # calculate the sum of word_count i  one class
        count_sum = 0
        for word, value in overall_count_dict[ana_class].items():
            count_sum += value
        # sort the dict in descending order
        sorted_dict = sorted(overall_count_dict[ana_class].items(), key=lambda d: d[1], reverse=True)
        i = 0
        train_file_word_count_overall.write(str(count_sum) + '\n')
        for temp_dict in sorted_dict:
            if temp_dict[0] == ' ':
                continue
            write_str = str(temp_dict[0]) + ' ' + str(int(temp_dict[1])) + '\n'
            train_file_word_count_overall.write(write_str)
            i += 1
            if i == 400:  # select the most appearing 400 words
                break
        train_file_word_count_overall.close()


train_main()  # construct word count for training
test_main()  # construct word count for testing
