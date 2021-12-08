import json
import matplotlib.pyplot as plt
import os
import sys

def read_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    
    return data

def compute_success(data):
    success = {}
    for record in data:
        country = record["dest_country"]
        if record["success"] == "yes":
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
    ax.set_ylim([0, 10])
    plt.show()

def gather_isps(data):
    isps = {}
    counter = 0
    dest_isps = {}
    for record in data:
        dest_country = record["dest_country"]
        isp_set = set(record["isp"])
            
        for index, country in enumerate(record["countries"]):
            if country == dest_country:
                isp = record["isp"][index]
                if isp in dest_isps.keys() and isp in isp_set:
                    dest_isps[isp] += 1
                    isp_set.remove(isp)
                else:
                    dest_isps[isp] = 1
        
        if (counter + 1) % 10 == 0:
            isps[dest_country] = dest_isps
            dest_isps = {}

        counter += 1
    return isps

def write_isps_to_file(isps, filename):
    pathfile = "../data/isp/" + "ISP-" + filename[19:]
    with open(pathfile, 'w') as f:
        json.dump(isps, f)

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
        print("Right use: [datafile path || folder path] [operation]")
        print("Available operations: plot_success, gather_isps, compare_detours")
    
    if sys.argv[2] == "plot_success":
        data = read_json(sys.argv[1])
        success_data = compute_success(data)
        plot_success_rate(success_data)
    elif sys.argv[2] == "gather_isps":
        data = read_json(sys.argv[1])
        isps = gather_isps(data)
        write_isps_to_file(isps, sys.argv[1])
    elif sys.argv[2] == "compare_detours":
        compare_detours(sys.argv[1])
    else:
        print("Invalid arguments")
        print("Right use: [datafile path || folder path] [operation]")
        print("Available operations: plot_success, gather_isps, compare_detours")
