# CIS 2348 Final Project Fall 2020.
# Dwayne Ellis
# Student ID: #######
# Final Project: This program manages the inventory of an electronics store.

import csv
import operator
import datetime

def print_data(list_dct):
    s = "{:<12}" * len(list_dct[0].keys())
    print(s.format(*list_dct[0].keys()))
    for item in list_dct:
        lst = [item[key] for key in item]
        print(s.format(*lst))

def write_csv(list_dct, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for item in list_dct:
            writer.writerow([item[key] for key in item])


# read data
with open('ManufacturerList.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    ManufacturerList = []
    for row in csv_reader:
        ManufacturerList.append({'ID': row[0], 'name': row[1], 'type': row[2], 'damaged': row[3]})

with open('PriceList.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    PriceList = []
    for row in csv_reader:
       PriceList.append({'ID': row[0], 'price': row[1]})

with open('ServiceDatesList.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    ServiceDatesList = []
    for row in csv_reader:
        ServiceDatesList.append({'ID': row[0], 'date': row[1]})

# print data
# print("\n    ManufacturerList:")
# print_data(ManufacturerList)
# print("\n    PriceList:")
# print_data(PriceList)
# print("\n    ServiceDatesList:")
# print_data(ServiceDatesList)

# 1) Processed Inventory Reports
# a.
FullInventory = ManufacturerList.copy()
# union of data
for item in FullInventory:
    item['price'] = 0
    item['date'] = ''
for i in range(len(FullInventory)):
    FullInventory[i]['price'] = PriceList[i]['price']
    FullInventory[i]['date'] = ServiceDatesList[i]['date']

# sort data by name
FullInventory.sort(key=operator.itemgetter('name'))

# save to file
write_csv(FullInventory, 'FullInventory.csv')

# b.
# Laptop
LaptopInventory = []
PhoneInventory = []
TowerInventory = []
for item in FullInventory.copy():
    item1 = item.copy()
    if item1['type'] == 'laptop':
        item1.pop('type')
        LaptopInventory.append(item1)
        continue
    if item['type'] == 'phone':
        item1.pop('type')
        PhoneInventory.append(item1)
        continue
    if item['type'] == 'tower':
        item1.pop('type')
        TowerInventory.append(item1)
        continue

LaptopInventory.sort(key=operator.itemgetter('ID'))
PhoneInventory.sort(key=operator.itemgetter('ID'))
TowerInventory.sort(key=operator.itemgetter('ID'))

# save to file
write_csv(LaptopInventory, 'LaptopInventory.csv')
write_csv(PhoneInventory, 'PhoneInventory.csv')
write_csv(TowerInventory, 'TowerInventory.csv')

# c.
PastServiceDateInventory = []
for item in FullInventory.copy():
    item1 = item.copy()
    if datetime.datetime.strptime(item1['date'], "%m/%d/%Y") < datetime.datetime.today():
        item1.pop('damaged')
        PastServiceDateInventory.append(item1)

LaptopInventory.sort(key=operator.itemgetter('date'))

# save to file
write_csv(PastServiceDateInventory, 'PastServiceDateInventory.csv')

# d.
DamagedInventory = []
for item in FullInventory.copy():
    item1 = item.copy()
    if item1['damaged'] == 'damaged':
        item1.pop('damaged')
        DamagedInventory.append(item1)

# save to file
write_csv(DamagedInventory, 'DamagedInventory.csv')


# 2) Interactive Inventory Query Capability
# i.
while True:
    name = input("Input manufacturer: ")
    if name == 'q':
        quit()
    type = input("Input type: ")
    if type == 'q':
        quit()
    query = []
    for item in FullInventory:
        if item['name'] == name and item['type'] == type:
            query.append(item)
    if query == []:
        print('No such item in inventory')

# ii.
    else:
        print('Your item is:')
        print_data(query)

        query1 = []
        for item in query:
            if item['damaged'] != 'damaged' and datetime.datetime.strptime(item['date'], "%m/%d/%Y") > datetime.datetime.today():
                query1.append(item)
        query1.sort(key=operator.itemgetter('price'))
        if query1 != []:
            current_price = query1[0]['price']

# iii.
            query2 = []
            for item in FullInventory:
                if (item['name'] != name) and (item['type'] == type) and (item['damaged'] != 'damaged') and\
                    (datetime.datetime.strptime(item['date'], "%m/%d/%Y") > datetime.datetime.today()) and\
                    (item['price'] > current_price):
                    query2.append(item)

            if query2 != []:
                print("\nYou may, also, consider:")
                print_data(query2)
