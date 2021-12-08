import json
import sys

def calculate_detours(data):
    for record in data:
        countries = record["countries"]
        auton_sys = record["as"]
        if len(set(countries)) == len(countries):
            record["detour"] = "no"
        
        for index, country in enumerate(countries):
            find = False
            if index == len(countries): continue
            for sindex, scountry in enumerate(countries[index+1:]):
                if country == scountry: continue
                smth = [index for index, char in enumerate(countries[sindex+index+1:]) if char == country]
                if len(smth) and auton_sys[index] != auton_sys[smth[0] + sindex + index + 1]:
                    if auton_sys[index] == "" or auton_sys[smth[0] + sindex + index + 1] == "":
                        record["detour"] = "possible"
                    else:
                        record["detour"] = "yes"
                    find = True
                    break
            if find: break
            record["detour"] = "no"
    return data


def read_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    
    return data

def write_data_to_file(data, filepath):
    filepath = filepath[:-5] + ".json"
    with open(filepath, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    data = read_json(sys.argv[1])
    updated_data = calculate_detours(data)
    write_data_to_file(updated_data, sys.argv[1])
