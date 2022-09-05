import json
import os
from gen_data import str_trans
import numpy as np
import pandas as pd


def over_lap(g_strs, a_strs):
    poses = [-1 for _ in range(len(g_strs))]
    for i, g_str in enumerate(g_strs):
        if g_str in a_strs:
            poses[i] = a_strs.index(g_str)
    return poses

def rho_cal(pos_array):
    ans = 0
    cnt = 0
    for i in range(len(pos_array)):
        if pos_array[i] >= 0:
           cnt += 1
           ans += (pos_array[i] - i) ** 2
    if cnt == 0:
        ans = 0
    elif cnt == 1:
        ans = 1 - ans
    else:
        ans = 1 - 6 * ans / (cnt * (cnt ** 2 - 1))
    return ans

def get_average(arr):
    print(arr)
    return np.sum(arr) / arr.shape[0]

if __name__ == '__main__':
    current_path = os.path.dirname(__file__)
    search_strings_path = os.path.join(current_path, "search_strings.txt")
    ask_results_path = os.path.join(current_path, "hw1.json")
    google_results_path = os.path.join(current_path, "google_results.json")
    with open(search_strings_path) as f:
        search_strings = f.readlines()
    with open(ask_results_path) as f:
        ask_results = json.load(f)
    with open(google_results_path) as f:
        google_results = json.load(f)

    for key in ask_results:
        value = ask_results[key]
        for i in range(len(value)):
            value[i] = value[i].replace('https://', '')
            value[i] = value[i].replace('http://', '')
    for key in google_results:
        value = google_results[key]
        for i in range(len(value)):
            value[i] = value[i].replace('https://', '')
            value[i] = value[i].replace('http://', '')

    str_trans(search_strings)

    queries = []
    index = 0
    averages = [0, 0, 0]
    for search_string in search_strings:
        index += 1
        query = []
        ask_result = ask_results[search_string]
        google_result = google_results[search_string]
        google_result_len = len(google_result)
        # print('ask: ', ask_result)
        # print('google: ', google_result)
        over_lap_poses = over_lap(google_result, ask_result)

        over_lap_num = 0
        for over_lap_pos in over_lap_poses:
            if over_lap_pos >= 0:
                over_lap_num += 1

        over_lap_percent = over_lap_num * 100.0 / google_result_len

        rho = rho_cal(over_lap_poses)

        averages[0] += over_lap_num
        averages[1] += over_lap_percent
        averages[2] += rho

        query = [f"Query {index}", over_lap_num, over_lap_percent, rho]
        query = np.asarray(query)
        queries.append(query)

    average_query = ['Average', averages[0] / 100, averages[1] / 100,
                     averages[2] / 100]
    average_query = np.asarray(average_query)
    queries.append(average_query)
    queries = np.asarray(queries)
    print(queries)

    save_path = os.path.join(current_path, 'hw1.csv')
    pd.DataFrame(queries).to_csv(save_path, header=None, index=None)



