from iptools import ipv4
import pandas as pd
import plotly.graph_objects as go
import socket
import sys
from traceroute import Traceroute

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


ip = sys.argv[1] if ipv4.validate_ip(sys.argv[1]) else socket.gethostbyname(sys.argv[1])
tracerouteLO = Traceroute(ip, country="LO")
hopsLO = tracerouteLO.traceroute()
# print_formatted_output(hopsLO)

dfLO = initialize_dataframe(hopsLO)
print(dfLO)

generate_map(dfLO)
