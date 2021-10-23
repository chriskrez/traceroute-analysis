from iptools import ipv4
import pandas as pd
import plotly.graph_objects as go
import socket
import sys
from traceroute import Traceroute


ip = sys.argv[1] if ipv4.validate_ip(sys.argv[1]) else socket.gethostbyname(sys.argv[1])
traceroute = Traceroute(ip, country="LO")
hops = traceroute.traceroute()
print(hops)

df = pd.DataFrame(columns=['hop', 'latitude', 'longitude'])
for hop in hops:
    df = df.append({'hop': hop["hop_num"], 'latitude': hop["latitude"], 'longitude': hop["longitude"]}, ignore_index=True)

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
