from datetime import date, datetime
from numpy import inf
from traceroute import Traceroute
import json
import requests
import time

def read_file(country):
    data = []
    with open("example_ips.txt") as file_object:
        for line in file_object:
            if line != "\n":
                ip = line.rstrip()
                traceroute = Traceroute(ip, country=country)
                hops = traceroute.traceroute()
                info_json = collect_info(ip, hops)
                data.append(info_json)
    write_file(data, country)

def collect_info(ip, hops):
    while True:
        dest_info = requests.get("http://ip-api.com/json/{}".format(ip))
        if int(dest_info.headers["X-Ttl"]) > 0:
            time.sleep(int(dest_info.headers["X-Rl"]))
            break
    
    info = {
        "dest_ip": ip,
        "dest_country": dest_info.json()["country"],
        "total_hops": hops[-1]["hop_num"],
        "countries": [],
        "rtt": [],
        "as": [],
        "isp": []
    }
                
    for hop in hops:
        if len(info["countries"]) == 0 or info["countries"][-1] != hop["country"]:
            info["countries"].append(hop["country"])
        info["rtt"].append(hop["rtt"])
        info["as"].append(hop["as"])
        info["isp"].append(hop["isp"])

    return info

def write_file(data, country):
    pathfile = "data/" + country + "-" + str(date.today().strftime("%d-%m-%Y")) + "-" + str(datetime.now().strftime("%H-%M")) + ".json"
    with open(pathfile, 'w') as f:
        json.dump(data, f)

read_file("LO")
