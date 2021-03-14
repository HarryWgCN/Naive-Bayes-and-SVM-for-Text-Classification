import os
from urllib.parse import urlparse
from xml.dom import minidom


def file_fill(file_dir, modified_dir):
    # traverse through the whole folder
    for root, dirs, files in os.walk(file_dir):
        if len(files) == 0:
            return
        for f in files:
            tmp_dir = modified_dir + '/' + f  # the folder storing the modified files
            ori_file_path = file_dir + '/' + f  # the original file_path
            file_source = open(ori_file_path, 'r', encoding='utf-8')
            modified_file = open(tmp_dir, 'w', encoding='utf-8')
            start_note = '<docs>\n'
            end_note = '</docs>'
            line_content = file_source.readlines()
            # add <docs> note for parsing and modify '&'
            modified_file.write(start_note)
            for lines in line_content:
                text = lines.replace('&', 'a')
                modified_file.write(text)
            modified_file.write(end_note)
            file_source.close()
            modified_file.close()


def file_read(file_dir, result_dir, url_dict, count_dict):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            print(f)
            modified_file_path = file_dir + "/" + f
            file_parse = minidom.parse(modified_file_path)
            root = file_parse.documentElement
            claim_content = root.getElementsByTagName("content")
            claim_url = root.getElementsByTagName("url")
            # cope with each url, specifying each class
            for index in range(0, len(claim_url)):
                if claim_url[index].firstChild is None or claim_content[index].firstChild is None:
                    continue
                # construct the class folder according to url
                url = urlparse(claim_url[index].firstChild.data)
                url_hostname = url.hostname.split('.')[0]
                if url_hostname in url_dict:
                    if not os.path.exists(result_dir + '/' + url_dict[url_hostname]):
                        os.makedirs(result_dir + '/' + url_dict[url_hostname])
                    # name by 1,2,3,4,5......
                    output_file_path = result_dir + f"/{url_dict[url_hostname]}/"
                    output_file_path += f"{str(count_dict[url_hostname])}.txt "
                    if count_dict[url_hostname] > 10000:
                        continue
                    count_dict[url_hostname] = count_dict[url_hostname] + 1
                    result_file = open(output_file_path, 'w', encoding='utf-8')
                    result_file.write(claim_content[index].firstChild.data)
                    result_file.close()


def main():
    classified_dir = "./sougou_modified"  # the path to store modified file from xml file
    if not os.path.exists(classified_dir):
        os.makedirs(classified_dir)
    result_dir = "./sougou_result"    # the path to store classified txt file
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # cope with the original file
    file_fill("./sougou_before2", classified_dir)

    # set a dict for determine the class from the url in file
    url_dict = {'auto': 'auto', 'it': 'it', 'health': 'health', 'edu':'education',
                'sports': 'sports', 'travel': 'travel', 'learning': 'learning', 'ent': 'entertainment',
                'career': 'career', 'cul': 'culture', 'mil': 'military', 'military': 'military',
                'house': 'house', 'yule': 'yule', 'women': 'fashion', 'lady': 'lady', 'eladies': 'lady',
                'media': 'media', 'gongyi': 'charity', '2008': 'Olympic',
                'finance': 'finance', 'tech': 'technology', 'money': 'finance'}
    count_dict = dict()
    for word, word_ in url_dict.items():
        count_dict[word] = int(1)

    # construct the required files
    file_read(classified_dir, result_dir, url_dict, count_dict)


main()
