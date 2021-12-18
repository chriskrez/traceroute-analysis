import json
import matplotlib.pyplot as plt
import os
import sys

def read_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    
    return data

def compute_success(folder):
    success = {}
    for file in os.listdir(folder):
        json_path = os.path.join(folder, file)
        data = read_json(json_path)
        for record in data:
            country = record["dest_country"]
            if record["success"] == "yes" and country != "Canada":
                if country in success.keys():
                    success[country] += 1
                else:
                    success[country] = 1
    return success

def plot_success_rate(data):
    names = list(data.keys())
    values = list(data.values())
    plt.bar(range(len(data)), values, tick_label=names)
    plt.xlabel("Destination Countries")
    plt.ylabel("Success rate")
    ax = plt.gca()
    ax.set_ylim([0, 300])
    plt.show()

def compare_isps(folder):
    isps = {}
    for file in os.listdir(folder):
        json_path = os.path.join(folder, file)
        data = read_json(json_path)
        for country in data:
            if country not in isps.keys():
                isps[country] = {}
                isps[country]["entered_country"] = 0
            
            record = data[country]
            isps[country]["entered_country"] += record["entered_country"]
            
            for isp in record:
                if isp == "entered_country": continue
                if isp in isps[country].keys():
                    isps[country][isp] += record[isp]
                else:
                    isps[country][isp] = record[isp]
    return isps

def normalize_isps(isps):
    for country in isps:
        record = isps[country]
        entered = record["entered_country"]
        for isp in record:
            if record[isp]:
                record[isp] = (record[isp] / entered) * 100
        record.pop("entered_country", None)

    return isps

def print_interesting_isps(isps):
    for country in isps:
        record = isps[country]
        for isp in record:
            if record[isp] > 40:
                print(country + " - ISP: " + isp + " - Percentage: " + str(round(record[isp], 2)))

def compare_detours(folder):
    detours = {}
    for file in os.listdir(folder):
        json_path = os.path.join(folder, file)
        data = read_json(json_path)
        for record in data:
            ip = record["dest_ip"]
            country = record["dest_country"]
            if record["detour"] == "yes":
                if ip in detours.keys():
                    detours[ip]["times"] += 1
                else:
                    detours[ip] = {}
                    detours[ip]["times"] = 1
                    detours[ip]["country"] = country
    for ip in detours:
        ip_dict = detours[ip]
        print(str(ip) + " (" + ip_dict["country"] + "):" + str(ip_dict["times"]))   

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid arguments")
        print("Right use: folder_path operation")
        print("Available operations: plot_success, compare_isps, compare_detours")
        exit(0)
    
    if sys.argv[2] == "plot_success":
        folder = sys.argv[1]
        success_data = compute_success(folder)
        plot_success_rate(success_data)
    elif sys.argv[2] == "compare_isps":
        isps = compare_isps(sys.argv[1])
        normalized = normalize_isps(isps)
        print_interesting_isps(normalized)
    elif sys.argv[2] == "compare_detours":
        compare_detours(sys.argv[1])
    else:
        print("Invalid arguments")
        print("Right use: folder_path operation")
        print("Available operations: plot_success, compare_isps, compare_detours")
