#!/usr/bin/python3
import generateJSON
import json

class Node():
	def __init__(self,info):
		self.info = info
		self.left_child = None
		self.right_child = None


def kdTree(point_list, k, depth = 0):
	axis = depth%k
	point_list.sort(key = lambda x: x['location'][axis])
	
	n = len(point_list)
	if n==1:
		node = Node(point_list[0])
		return node
	elif n==2:
		node = Node(point_list[0])
		node.left_child = kdTree(point_list[1:],k,depth+1)
		pass
	else:
		median = n//2
		node = Node(point_list[median])
		node.left_child = kdTree(point_list[:median], k, depth+1)
		node.right_child = kdTree(point_list[median + 1:] , k, depth+1)

		return node







def generateGraph():
	with open('worldcitiespop.json', 'r', encoding="utf8") as json_file:
		jfile = json.load(json_file)
		other = []
		for city in jfile:
			if(float(city['Population'])>=10000):
				#print(city['City'])
				other.append(city)

		tree = kdTree(other,3)
		f = open("out.txt",'w')
		f.write("digraph { concentrate=true ")
		f.write(printTree(tree,"out.txt"))


def printTree(node,file):
	if node != None:
		out = ""
		#f = open(file,'a')
		print("Node " + node.info['City'] + " goes to ",end='')
		if node.left_child != None:
			print(node.left_child.info['City'] + " and ", end='')
		if node.right_child != None:
			print(node.right_child.info['City'])	
		print()
		if node.left_child != None:
			#f.write(node.info['City'].replace("-","").replace(" ","") + " -> " + node.left_child.info['City'].replace("-","").replace(" ","") + "\n")
			out = out + (node.info['City'].replace("-","").replace(" ","") + " -> " + node.left_child.info['City'].replace("-","").replace(" ","") + "\n")+printTree(node.left_child,file)
		if node.right_child != None:
			#f.write(node.info['City'].replace("-","").replace(" ","") + " -> " + node.right_child.info['City'].replace("-","").replace(" ","") + "\n")
			out = out + (node.info['City'].replace("-","").replace(" ","") + " -> " + node.right_child.info['City'].replace("-","").replace(" ","") + "\n")+printTree(node.right_child,file)
		#f.close()
		return out




generateJSON.processFile("worldcitiespop")
#generateGraph()

