from gen_data import str_trans, search_key
import os
import json
import time

if __name__ == '__main__':
    current_path = os.path.dirname(__file__)
    search_strings_file_path = os.path.join(current_path, 'search_strings.txt')
    with open(search_strings_file_path) as f:
        search_strings = f.readlines()
    str_trans(search_strings)
    search_key(search_strings[0])