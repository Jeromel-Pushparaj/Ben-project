import json


# Path to the JSON file
json_file_path = "D:\\linuxplayground\\Ben project conf\\data.json"

# Read data from the JSON file
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

# Print the data
admintoken = data['adminToken']

print(admintoken)