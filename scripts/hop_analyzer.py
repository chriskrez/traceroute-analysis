from iptools import ipv4
import pandas as pd
import plotly.graph_objects as go
import socket
import sys
from traceroute import Traceroute
import requests

def initialize_dataframe(hops):
    df = pd.DataFrame(columns=['Hop', 'Latitude', 'Longitude', 'Country', 'ISP', 'RTT'])
    counter = -1
    for hop in hops:
        if counter != hop["hop_num"]:
            df = df.append({'Hop': hop["hop_num"],
                            'Latitude': hop["latitude"],
                            'Longitude': hop["longitude"],
                            'Country': hop["country"],
                            'ISP': hop["isp"],
                            'AS': hop["as"].split()[0] if len(hop["as"]) > 0 else "",
                            'RTT': hop["rtt"]},
                            ignore_index=True)
        counter = hop["hop_num"]

    return df

def print_formatted_output(hops):
    for hop in hops:
        print("Hop number: ", hop["hop_num"])
        print("IP address: ", hop["ip_address"])
        print("Country: ", hop["country"])
        print("RTT: ", hop["rtt"])
        print()

def generate_map(df):
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = df.Longitude,
        lat = df.Latitude,
        marker = { 'size': 14 },
        text = df.Hop
    ))

    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 1})
    fig.show()

if __name__ == '__main__':
    dest_ip = sys.argv[1] if ipv4.validate_ip(sys.argv[1]) else socket.gethostbyname(sys.argv[1])
    tracerouteLO = Traceroute(dest_ip, country="LO")
    hopsLO = tracerouteLO.traceroute()
    # print_formatted_output(hopsLO)

    dfLO = initialize_dataframe(hopsLO)
    print(dfLO)

    last_ip = hopsLO[-1]["ip_address"]
    if last_ip != dest_ip:
        print()
        original_country = requests.get("http://ip-api.com/json/{}".format(dest_ip))
        print("Desired destination ip: " + dest_ip)
        print("Desired destination country: " + original_country.json()["country"])

        reached_country = requests.get("http://ip-api.com/json/{}".format(last_ip))
        print("Destination not reached")
        print("Traceroute ended to: " + reached_country.json()["country"])

    generate_map(dfLO)
