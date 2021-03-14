import os
classes = 10
file_start = 1
file_end = 10000

for ana_class in range(1, classes + 1):  # for each class
    for ana_file in range(file_start, file_end + 1):  # for each file (ordered naming)
        train_file_split = open(f'./data/train_data_split/{ana_class}/{ana_file}.txt', 'r', encoding='utf-8')
        train_file_aggregate_path = f'./data/train_data_aggregate/{ana_class}/{ana_file}.txt'
        train_file_aggregate_dir = f'./data/train_data_aggregate/{ana_class}'
        if not os.path.exists(train_file_aggregate_dir):
            os.makedirs(train_file_aggregate_dir)
        train_file_aggregate = open(train_file_aggregate_path, 'w', encoding='utf-8')
        lines = train_file_split.readlines()  # read all lines(containing the word and its flag
        # extract nouns from cut file
        for line in lines:
            if 'n' in line:  # only select nouns out
                pair = line.split('\t')
                noun = pair[0]
                train_file_aggregate.write(f'{noun} ')
        train_file_aggregate.write('\n')
        train_file_split.close()
        train_file_aggregate.close()
