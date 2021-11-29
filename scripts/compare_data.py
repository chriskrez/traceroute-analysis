import json
import matplotlib.pyplot as plt
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

if __name__ == '__main__':
    data = read_json(sys.argv[1])
    success_data = compute_success(data)
    plot_success_rate(success_data)
