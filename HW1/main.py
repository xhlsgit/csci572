from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json

def search_key(key_words):
    ans_links = []
    key_words = key_words.replace(' ', '%20')
    req = Request("https://www.ask.com/web?q=" + key_words)
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, features="html.parser")

    search_filter = dict()
    search_filter["class"] = "PartialSearchResults-item-title"
    results = soup.findAll('div', search_filter)
    for result in results:
        a_blank = result.findAll('a')
        # print(a_blank[0])
        # print("==========================================")
        assert len(a_blank[0]) == 1
        ans_links.append(a_blank[0].get('href'))
    # print(ans_links)
    return ans_links

    # links = []
    # search_filter = dict()
    # search_filter['class'] = 'PartialSearchResults-item-title-link result-link'
    # for link in soup.findAll('a', search_filter):
    #     links.append(link.get('href'))
    # assert len(links) >= 10
    # return links[:10]

def str_trans(strings):
    for i in range(len(strings)):
        strings[i] = strings[i].replace('\n', '')

if __name__ == '__main__':
    with open("./HW1/search_strings.txt") as f:
        search_strings = f.readlines()
    str_trans(search_strings)
    # search_key(search_strings[0])
    results = dict()
    index = 0
    for key_str in search_strings:
        results[key_str] = search_key(key_str)
        index += 1
        print(index)
    # print(results)
    # save
    with open('data.json', 'w') as f:
        json_object = json.dump(results, f, indent=4)






