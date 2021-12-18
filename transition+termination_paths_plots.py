import os
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import json

def create_datalists():
    base_dir_LO= "../data/traceroute/LO/"
    base_dir_RU= "../data/traceroute/RU/"
    LO_data_list = []
    RU_data_list = []

    print(os.listdir(base_dir_LO))

    for file in os.listdir(base_dir_LO):
        json_path_LO = os.path.join(base_dir_LO, file)
        
        with open(json_path_LO) as json_file:
            data = json.load(json_file)

        LO_data_list.append(data)

    for file in os.listdir(base_dir_RU):
        json_path_RU = os.path.join(base_dir_RU, file)

        with open(json_path_RU) as json_file:
            data = json.load(json_file)
        
        RU_data_list.append(data)
        
    return LO_data_list, RU_data_list

def compute_path_transits(data_origin,destination):    
    country_routes={}
    for data in data_origin:
        # print(data)
        for target_ip in data:
            
            if target_ip["dest_country"] == destination:
                for country in list(set(target_ip["countries"])):
                    if country not in country_routes:
                        country_routes[country]=1
                    else:
                        country_routes[country]+=1 
                 
    country_routes = {country: round(counts / sum(country_routes.values())*100,3) for country, counts in country_routes.items()}
    return country_routes

def compute_path_terminations(data_origin,destination):
    country_routes={}
    for data in data_origin:
        for target_ip in data:

            if target_ip["dest_country"] == destination and target_ip["countries"]:
                terminated_country=target_ip["countries"][-1]
                if terminated_country not in country_routes:
                    country_routes[terminated_country]=1
                else:
                    country_routes[terminated_country]+=1 
                    
    country_routes = {country: round(counts / sum(country_routes.values())*100,3) for country, counts in country_routes.items()}  
    return country_routes


def plotter_transits(results,origin):

    countries_enum=["Germany","United States","Cyprus","Egypt","Iran","Russia","North Korea","Vietnam"]
    
    for count,studied_countries in enumerate(results):
        if origin == "Local":
            studied_countries.pop("Netherlands")
        elif origin == "Russia":
            studied_countries.pop("Russia")
        fig = plt.figure(figsize=(14,9))
        ax = fig.add_axes([0.1,0.1,0.85,0.85])
        countries = list(studied_countries.keys())
        percentage = list(studied_countries.values())
        df=pd.DataFrame({"countries":countries,"percentage":percentage})
        df_sorted=df.sort_values("percentage",ascending=False)
        ax.bar("countries","percentage",data=df_sorted)
        plt.title(f"Percentage of  transit paths \n Origin = {origin} -- Destination = {countries_enum[count]} ")
        plt.show()

def plotter_terminations(results,origin):

    countries_enum=["Germany","United States","Cyprus","Egypt","Iran","Russia","North Korea","Vietnam"]
    
    for count,studied_countries in enumerate(results):
        fig = plt.figure(figsize=(14,9))
        ax = fig.add_axes([0.1,0.1,0.85,0.85])
        countries = list(studied_countries.keys())
        percentage = list(studied_countries.values())
        df=pd.DataFrame({"countries":countries,"percentage":percentage})
        df_sorted=df.sort_values("percentage",ascending=False)
        ax.bar("countries","percentage",data=df_sorted)
        plt.title(f"Percentage of  paths that terminates in each country \n Origin = {origin} -- Destination = {countries_enum[count]} ")
        plt.show()
            

if __name__ == '__main__':
    
    LO_data_list ,RU_data_list = create_datalists()
    
    countries_enum=["Germany","United States","Cyprus","Egypt","Iran","Russia","North Korea","Vietnam"]
    
    LO_transit_results=[]
    RU_transit_results=[]
    LO_termination_results=[]
    RU_termination_results=[]

    for country in countries_enum:
        LO_transit_results.append(compute_path_transits(LO_data_list,country))
        RU_transit_results.append(compute_path_transits(RU_data_list,country))

        LO_termination_results.append(compute_path_terminations(LO_data_list,country))
        RU_termination_results.append(compute_path_terminations(RU_data_list,country))



    plotter_transits(LO_transit_results,"Local")
    plotter_transits(RU_transit_results,"Russia")

    plotter_terminations(LO_termination_results,"Local")
    plotter_terminations(RU_termination_results,"Russia")
