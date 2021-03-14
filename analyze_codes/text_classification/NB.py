import math

classes = 10
file_start = 5001
file_end = 10000


def main():
    success_dict = dict()
    wrongly_out = dict()
    wrongly_from_other = dict()
    for i in range(1, 11):
        success_dict[i] = float(0)
        wrongly_out[i] = float(0)
        wrongly_from_other[i] = float(0)
    for test_class in range(1, classes + 1):
        for test_file in range(file_start, file_end + 1):
            # input test_file
            test_file_content = open(f'./data/train_data_aggregate/{test_class}/{test_file}.txt', 'r', encoding='utf-8')
            content = test_file_content.readlines()
            test_word_list = list()
            # form test file word list
            for line in content:
                content_split = line.split(' ')
                for word in content_split:
                    test_word_list.append(word)
            # now compute NB possibility values with train_file
            max_p = float(-1.0)
            class_decide = -1
            for train_class in range(1, classes + 1):
                train_file_word_count = open(f'./data/train_data_word_count/{train_class}.txt', 'r', encoding='utf-8')
                train_content = train_file_word_count.read()
                # get the words with their counting recorded in word count(400 most appearing word_count in a class)
                train_words_dict, sum_count = get_words(train_content)
                # count the num of words from test_file that appear in the train_words_dict
                temp_p = compute_bayes(test_word_list, train_words_dict, sum_count)
                # compare p to find the highest possibility
                if temp_p > max_p or max_p == -1.0:
                    max_p = temp_p
                    class_decide = train_class
            # print(str(test_class) + ' classified as ' + str(class_decide) + '\n')
            if class_decide == test_class:
                # print("{:4} {:4} {:!^20}\n".format(str(test_class), str(class_decide), "!"))
                success_dict[class_decide] += 1
            else:
                # print("{:4} wrongly classified as {:4} {:!^20}\n".format(str(test_class), str(class_decide), "!"))
                wrongly_out[test_class] += 1
                wrongly_from_other[class_decide] += 1
        print('Success rate as    ' + str(success_dict[test_class] / (file_end - file_start + 1)) +
              f' for class {test_class}\n')
    recall_all = float(0)
    precision_all = float(0)
    for i in range(1, 11):
        print('Recall rate as    ' + str(success_dict[i] / (success_dict[i] + wrongly_out[i])) + f' for class {i}')
        recall_all += success_dict[i] / (success_dict[i] + wrongly_out[i])
        print('Precision rate as ' + str(success_dict[i] / (success_dict[i] + wrongly_from_other[i])) +
              f' for class {i}\n')
        precision_all += success_dict[i] / (success_dict[i] + wrongly_from_other[i])
    print("!!!!!!!!!!!!!!!!!!!!!\nFor all, "
          f"Recall rate as {recall_all / 10}\n"
          f"Precision rate as       {precision_all / 10}")


def count(word_list):
    count_dict = dict()
    for word in word_list:
        if word == '\n':
            continue
        if word in count_dict:
            count_dict[str(word)] += 1  # initialize a record for this word
        else:
            count_dict[str(word)] = 1  # add one count for this word
    return count_dict


def compute_bayes(test_word_list, train_words_dict, sum_count):
    p = 0
    # test_word_count = count(test_word_list)
    # using mixed model and log optimizing
    # considering the prior probability to be the same for each class
    coped_note = dict()
    for word, p in train_words_dict.items():
        coped_note[word] = 0
    for word in test_word_list:
        # existing in train_file, then multiply the p
        if word in train_words_dict:
            if not coped_note[word]:
                p += math.log(train_words_dict[word])
                # one word in test_file dealt with once
                coped_note[word] += 1
        # not existing in train_file, then multiply with lapels
        else:
            p += math.log(1 / (sum_count + classes))
    return p


def get_words(content):
    words_dict = dict()
    sum_count = 0  # the sum of appearing times
    content_split = content.split('\n')
    # get word with its counting at each line
    for line in content_split:
        line_split = line.split(' ')
        if len(line_split) < 2:
            continue
        words_dict[line_split[0]] = line_split[1]
        sum_count += float(line_split[1])
    for word_tuple in words_dict.items():
        words_dict[word_tuple[0]] = float(word_tuple[1]) / sum_count
    return words_dict, sum_count


main()
