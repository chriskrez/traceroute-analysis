from datetime import date, datetime
from numpy import inf
from traceroute import Traceroute
import json
import requests
import sys
import time

def read_file(country):
    data = []
    with open("ips.txt") as file_object:
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
        dest_info = requests.get(f"http://ip-api.com/json/{ip}")
        if int(dest_info.headers["X-Rl"]) == 0:
            time.sleep(int(dest_info.headers["X-Ttl"]))
        else:
            break
    
    info = {
        "dest_ip": ip,
        "dest_country": dest_info.json()["country"] if len(dest_info.json()["country"]) > 0 else "",
        "total_hops": hops[-1]["hop_num"] if hops[-1]["hop_num"] > 0 else "",
        "success": "yes" if ip == hops[-1]["ip_address"] else "no",
        "ips": [],
        "countries": [],
        "rtt": [],
        "as": [],
        "isp": [],
        "detour": ""
    }

    counter = -1           
    for hop in hops:
        if counter != hop["hop_num"]:
            info["ips"].append(hop["ip_address"])
            info["countries"].append(hop["country"])
            info["rtt"].append(hop["rtt"])
            info["as"].append(hop["as"])
            info["isp"].append(hop["isp"])
        counter = hop["hop_num"]
    
    # info["detour"] = "yes" if len(set(info["countries"])) < len(info["countries"]) else "no"

    return info

def write_file(data, country):
    pathfile = "../data/" + country + "-" + str(date.today().strftime("%d-%m-%Y")) + "-" + str(datetime.now().strftime("%H-%M")) + ".json"
    with open(pathfile, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    read_file(sys.argv[1])
