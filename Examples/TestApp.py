import PySense
import os
import json

token = PySense.authenticate('localhost:8081', 'nathan.giusti@sisense.com', 'qweQWE123!')
path = 'C:\\Users\\nathan.giusti\\Desktop\\dashboards'

for root, directories, files in os.walk(path):
    for filename in files:
        with open(os.path.join(root, filename)) as file:
            data = file.read()
        print(data)
        PySense.post_dashboards_import_bulk(data, importFolder="MercuryGate")
        exit(0)

