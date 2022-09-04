from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import os
import time

def search_key(key_words):
    ans_links = []
    key_words = key_words.replace(' ', '%20')
    url = f"https://www.ask.com/web?q={key_words}"
    # print(url)
    req1 = Request(url)
    html_page1 = urlopen(req1)

    soup1 = BeautifulSoup(html_page1, features="html.parser")

    search_filter = dict()
    search_filter["class"] = "PartialSearchResults-item-title"
    results1 = soup1.findAll('div', search_filter)
    for result in results1:
        # print(result)
        a_blank = result.findAll('a')
        # print(a_blank[0])
        # print("==========================================")
        assert len(a_blank[0]) == 1
        ans_link = a_blank[0].get('href')
        ans_link = ans_link.replace('https://', '')
        ans_link = ans_link.replace('http://', '')
        ans_links.append(ans_link)
    # print(ans_links)
    if len(ans_links) >= 10:
        return ans_links[:10]
    else:
        print("Length less than 10!")
        return ans_links

def str_trans(strings):
    for i in range(len(strings)):
        strings[i] = strings[i].replace('\n', '')

if __name__ == '__main__':
    current_path = os.path.dirname(__file__)
    search_strings_file_path = os.path.join(current_path, 'search_strings.txt')
    with open(search_strings_file_path) as f:
        search_strings = f.readlines()
    str_trans(search_strings)
    # search_key(search_strings[0])
    results = dict()
    index = 0
    for key_str in search_strings:
        results[key_str] = search_key(key_str)
        index += 1
        print(index)
        time.sleep(3)
    # print(results)
    # save
    save_ask_results_path = os.path.join(current_path, 'hw1.json')
    with open(save_ask_results_path, 'w') as f:
        json_object = json.dump(results, f, indent=4)






