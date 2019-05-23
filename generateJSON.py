import csv
import json
import os
from haversine import haversine, Unit
import math


def processFile(path):
	csvfile = open(path+'.csv','r',encoding="utf8")
	jsonfile = open(path+'.json', 'w')

	fieldnames = ("FirstName", "LastName", "IDNumber", "Message")
	reader = csv.DictReader(csvfile)
	print("Generating JSON")
	i = 0
	#jsonfile.write('{ "data": [ \n')
	#countryDict = {}
	countryDict = []
	for row in reader:
		if len(countryDict)==3000: break;
		if row['Population'] != "":
			t = row
			city = t['Country']
			#t.pop('Country', None)
			t.pop('AccentCity')
			t.pop('Region')
			x = math.cos(float(row['Latitude'])) * math.cos(float(row['Longitude']))
			y = math.cos(float(row['Latitude'])) * math.sin(float(row['Longitude']))
			z = math.sin(float(row['Latitude']))
			location = (x,y,z)
			t['location'] = location
			countryDict.append(t)






			#if i==100: break
			#if i!=0:
				#jsonfile.write(',')
			#json.dump(countryDict, jsonfile)
			#jsonfile.write('\n')
			i = i + 1

	#for cityCode in countryDict:
		#print(countryDict.get(cityCode))
	jsonfile.write('[')
	for key in countryDict:
		json.dump(key,jsonfile)
		jsonfile.write(",\n")

	jsonfile.seek(jsonfile.tell() - 2, os.SEEK_SET)
	jsonfile.write('\n')
	jsonfile.write(']')
	#json.dump(countryDict,jsonfile)


	#jsonfile.write("]\n}")
	return 0