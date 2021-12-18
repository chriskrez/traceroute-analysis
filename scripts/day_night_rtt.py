import os
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import json
def create_datalists():
    base_dir_LO= "../data/traceroute/LO/"
    
    LO_day_data_list = []
    LO_night_data_list = []
    

    for file in os.listdir(base_dir_LO):
        json_path_LO = os.path.join(base_dir_LO, file)
        
        with open(json_path_LO) as json_file:
            data = json.load(json_file)
        if 'day' in file:    
            LO_day_data_list.append(data)
        elif 'night' in file:
            LO_night_data_list.append(data)
    return LO_day_data_list,LO_night_data_list




# def create_datalists():
#     base_dir = '../data'
#     LO_day_data_list = []
#     LO_night_data_list = []
#     for file in os.listdir(base_dir):
#         if 'json' in file:
#             if 'LO' and 'day' in file:
#                 json_path = os.path.join(base_dir, file)
#                 json_data = pd.read_json(json_path, lines=True)
#                 LO_day_data_list.append(json_data)
#             elif 'LO' and 'night' in file:
#                 json_path = os.path.join(base_dir, file)
#                 json_data = pd.read_json(json_path, lines=True)
#                 LO_night_data_list.append(json_data)
#     return LO_day_data_list,LO_night_data_list


def compute_rtt(data_origin,destination):    
    country_rtt=[]

    for data in data_origin:
        for target_ip in data:
            if target_ip["dest_country"] == destination and target_ip["success"] == "yes" :
                country_rtt.append(float(target_ip["rtt"][-1][:-3]))  
    return country_rtt




def plotter_rtt(day_data,night_data):

    countries_enum=["Germany","United States","Iran","Russia","Vietnam"]
    day_mean_rtt=[]
    night_mean_rtt=[]
    
    for rtt in day_data:
        if rtt :
            day_mean_rtt.append(mean(rtt))
 
    for rtt in night_data:
        if rtt :
            night_mean_rtt.append(mean(rtt))

    X = np.arange(len(countries_enum))
    fig = plt.figure(figsize=(14,9))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    ax.bar(X-0.2, day_mean_rtt, color = 'b', width = 0.4, label='date time RTT')
    ax.bar(X+0.2, night_mean_rtt, color = 'r', width = 0.4, label='night time RTT')
    plt.xticks(X,countries_enum)
    plt.xlabel("Destinations countries")
    plt.ylabel("Mean round trip time(ms)")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    
    countries_enum=["Germany","United States","Cyprus","Egypt","Iran","Russia","North Korea","Vietnam"]
    LO_day_data_list ,LO_night_data_list = create_datalists()
    print(LO_day_data_list)
    print(LO_day_data_list)
    LO_day_results=[]
    LO_night_results=[]
    for country in countries_enum:
        LO_day_results.append(compute_rtt(LO_day_data_list,country))
        LO_night_results.append(compute_rtt(LO_night_data_list,country))
        
    plotter_rtt(LO_day_results,LO_night_results)

