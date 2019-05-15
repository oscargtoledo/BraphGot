import csv
import json



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
		if row['Population'] != "":
			t = row
			city = t['Country']
			t.pop('Country', None)
			t.pop('AccentCity')
			t.pop('Region')
			'''if city in countryDict:
				countryDict[city].append(t)
			else:
				countryDict[city] = []
				countryDict[city].append(t)'''
			countryDict.append(t)






			#if i==100: break
			#if i!=0:
				#jsonfile.write(',')
			#json.dump(countryDict, jsonfile)
			#jsonfile.write('\n')
			i = i + 1

	#for cityCode in countryDict:
		#print(countryDict.get(cityCode))


	json.dump(countryDict,jsonfile)


	#jsonfile.write("]\n}")
	return 0