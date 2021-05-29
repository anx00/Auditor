from pymongo import MongoClient
import json


def save_data_mongo(data):

    data_aps = data[0]
    data_devices = data[1]
    data_connected_devices = data[2]

    mongo_url = 'mongodb://localhost'
    client = MongoClient(mongo_url)
    db = client['server']
    collection_ap = db['access_point']
    collection_devices = db['devices']
    collecion_connected_devices = db['connected_devices']

    #Save APs Info
    json_aps = json.loads(data_aps)
    if json_aps != []:
        for element in json_aps:
            flag = collection_ap.find({'bssid': element['fields']['bssid'],
                                                 'device_id': element['fields']['device_id']}).count() > 0
            if flag == False:
                collection_ap.insert_one(element['fields'])


    #Save Local Devices Info
    json_devices = json.loads(data_devices)
    if json_devices != []:
        for element in json_devices:
            flag = collection_devices.find({'mac': element['fields']['mac'],
                                       'device_id': element['fields']['device_id']}).count() > 0
            if flag == False:
                collection_devices.insert_one(element['fields'])


    #Save Connected Devices Info
    json_connected_devices = json.loads(data_connected_devices)
    if json_connected_devices != []:
        for element in json_connected_devices:
            flag = collecion_connected_devices.find({'mac_device': element['fields']['mac_device'],
                                            'device_id': element['fields']['device_id']}).count() > 0
            if flag == False:
                collecion_connected_devices.insert_one(element['fields'])
