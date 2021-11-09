from iptools import ipv4
import pandas as pd
import plotly.graph_objects as go
import socket
import sys
from traceroute import Traceroute


ip = sys.argv[1] if ipv4.validate_ip(sys.argv[1]) else socket.gethostbyname(sys.argv[1])
traceroute = Traceroute(ip, country="LO")
hops = traceroute.traceroute()

for hop in hops:
    print("Hop number: ", hop["hop_num"])
    print("IP address: ", hop["ip_address"])
    print("Country: ", hop["country"])
    print("RTT: ", hop["rtt"])
    print()

df = pd.DataFrame(columns=['hop', 'latitude', 'longitude', 'country', 'rtt'])
counter = -1
for hop in hops:
    if counter != hop["hop_num"]:
        df = df.append({'hop': hop["hop_num"], 'latitude': hop["latitude"], 'longitude': hop["longitude"], 'country': hop["country"], 'rtt': hop["rtt"]}, ignore_index=True)
    counter = hop["hop_num"]
print(df)

fig = go.Figure()
fig.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = df.longitude,
    lat = df.latitude,
    marker = { 'size': 14 },
    text = df.hop
))

fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 1})
fig.show()
