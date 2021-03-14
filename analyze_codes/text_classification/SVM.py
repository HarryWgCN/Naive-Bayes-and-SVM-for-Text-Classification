# -*- coding:utf-8 -*-
# -*- coding: cp936 -*-
from sklearn import svm
from sklearn.metrics import confusion_matrix, precision_score, recall_score

# assign a different number for each word to distinguish them
# and to use it in svc
from sklearn.model_selection import cross_val_predict

num_to_word_distribute = dict()

count = 0

train_label = list()
train_vector = list()
train_dir = './data/train_data_word_count'

# to form training vector and label
for train_class in range(1, 11):
    train_file_path = train_dir + f'/{train_class}.txt'
    train_file_ = open(train_file_path, 'r', encoding='utf-8')
    content_line_get = train_file_.readline()
    content_lines = train_file_.readlines()
    train_file_.close()
    for content_line in content_lines:
        content_line = content_line.strip('\n')
        content_list = content_line.split(' ')  # split by whitespace
        if content_list[0] not in num_to_word_distribute:
            num_to_word_distribute[content_list[0]] = count
            count += 1
        for i in range(1, int(float(content_list[1]) // 100 + 2)):
            train_vector.append([num_to_word_distribute[content_list[0]], 1])
            train_label.append(train_class)
    print(f'{train_class} finished training')
# train
clf = svm.SVC(C=1, kernel='rbf', gamma=0.1, decision_function_shape='ovr')
clf.fit(train_vector, train_label)

# to form test vector with its label
test_dir = './data/train_data_word_count_test'
precision_rate = float(0)
recall_rate = float(0)
for test_class in range(1, 11):
    test_vector = list()
    test_label = list()
    test_file_path = train_dir + f'/{test_class}.txt'

    test_file_ = open(test_file_path, 'r', encoding='utf-8')
    content_line_get = test_file_.readline()
    content_lines = test_file_.readlines()
    test_file_.close()
    for content_line in content_lines:
        content_line = content_line.strip('\n')
        content_list = content_line.split(' ')  # split by whitespace
        if content_list[0] not in num_to_word_distribute:
            num_to_word_distribute[content_list[0]] = count
            count += 1
        # record word with its label
        for i in range(1, int(float(content_list[1]) // 300 + 2)):
            test_vector.append([num_to_word_distribute[content_list[0]], 1])
            test_label.append(test_class)
    # to show the result of testing for this class
    predicted_y = clf.predict(test_vector)
    tn, fp, fn, tp = confusion_matrix(test_label, predicted_y).ravel()
    precision_score = tp / (tp + fp)
    precision_rate += precision_score
    recall_score = tp / (tp + fn)
    recall_rate += recall_score
# show overall result
print(f'Overall success rate is {precision_rate / 10}')
print(f'Overall recall rate is  {recall_rate / 10}')

