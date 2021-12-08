import json
import os
import sys

def read_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    
    return data

def gather_isps(data):
    isps = {}
    dest_isps = {}
    counter, entered_country = 0, 0
    flag = True
    for record in data:
        dest_country = record["dest_country"]
        isp_set = set(record["isp"])
            
        for index, country in enumerate(record["countries"]):
            if country == dest_country:
                isp = record["isp"][index]
                if flag:
                    entered_country += 1
                    flag = False

                if isp in dest_isps.keys() and isp in isp_set:
                    dest_isps[isp] += 1
                    isp_set.remove(isp)
                elif isp in isp_set:
                    dest_isps[isp] = 1
                    isp_set.remove(isp)
        
        if (counter + 1) % 10 == 0:
            isps[dest_country] = dest_isps
            isps[dest_country]["entered_country"] = entered_country
            dest_isps = {}
            entered_country = 0
        
        flag = True
        counter += 1
    return isps

def write_isps_to_file(isps, filename, country):
    pathfile = "../data/isp/" + str(country) + "ISP-" + filename
    with open(pathfile, 'w') as f:
        json.dump(isps, f)

folder = sys.argv[1]
country = folder[-3:]
for file in os.listdir(folder):
    json_path = os.path.join(folder, file)
    data = read_json(json_path)
    isps = gather_isps(data)
    write_isps_to_file(isps, file, country)
