#!/usr/bin/python3
import time
from itertools import (repeat, starmap)
from operator import (add)

from staticmap import CircleMarker, StaticMap, Line

import generateJSON
import json
from haversine import haversine, Unit


class Node():
    def __init__(self, info):
        self.info = info
        self.left_child = None
        self.right_child = None
    def __repr__(self):
        return self.info['City']


def kdTree(point_list, k, depth=0):
    axis = depth % k
    point_list.sort(key=lambda x: float(x['location'][axis]))
    '''if axis==1:
        point_list.sort(key=lambda x: float(x['Latitude']))
    else:
        point_list.sort(key=lambda x: float(x['Longitude']))'''
    n = len(point_list)
    #print(point_list)
    if n == 1:
        node = Node(point_list[0])
        return node
    elif n == 2:
        node = Node(point_list[0])
        node.left_child = kdTree(point_list[1:], k, depth + 1)

        pass
    else:
        median = n // 2
        node = Node(point_list[median])
        node.left_child = kdTree(point_list[:median], k, depth + 1)
        node.right_child = kdTree(point_list[median + 1:], k, depth + 1)


        return node


def closeNodes(root, node, distance, depth=0):
    outList = []
    k = 3
    latlon = (float(node['Latitude']),float(node['Longitude']))
    axis = depth % k
    if root is None:
        return outList
    else:
        '''print(str(depth) + " at " + str(root.info['City']) + " with childs ", end='')
        if root.left_child is not None: print(root.left_child)
        if root.right_child is not None: print(root.right_child)
        print("\n")'''
        '''print("--------")
        print(root)
        
        print("--------")'''
        if float(root.info['location'][axis]) > float(node['location'][axis]):
            #print("going left from " + root.info['City'])
            outList.extend(closeNodes(root.left_child, node, distance, depth+1))
            if float(root.info['location'][axis]) - float(node['location'][axis]) < distance * 3:

                #print("also left from " + root.info['City'])
                outList.extend(closeNodes(root.right_child, node, distance, depth+1))
        elif float(root.info['location'][axis]) < float(node['location'][axis]):
            #print("going right from " + root.info['City'])
            outList.extend(closeNodes(root.right_child, node, distance, depth+1))
            if float(node['location'][axis]) - float(root.info['location'][axis]) < distance * 3:
                #print("also right from " + root.info['City'])
                outList.extend(closeNodes(root.left_child, node, distance, depth + 1))

        '''else:
            pass'''
        #print(node['City'] + " distance to " + root.info['City'] + " = " + str(haversine((float(root.info['Latitude']), float(root.info['Longitude'])), latlon)))
        if haversine((float(root.info['Latitude']), float(root.info['Longitude'])), latlon) <= distance:
            #print("Adding " + root.info['City'])
            outList.append(root)

        return outList

def generateGraph():
    with open('worldcitiespop.json', 'r', encoding="utf8") as json_file:
        m = StaticMap(1000, 1000, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
        jfile = json.load(json_file)
        other = []
        for city in jfile:
            if float(city['Population']) >= 100000:
                # print(city['City'])
                other.append(city)

        tree = kdTree(other, 3)
        #f = open("out.txt", 'w')
        #f.write("digraph { concentrate=true ")
        #f.write(printTree(tree, "out.txt"))
        #print(jfile[0])
        #print(jfile[0]['location'][0])
        n = len(other)
        i = 0
        start = time.time()
        #for city in other:
        '''city = jfile[0]
        adj = closeNodes(tree,city,300)
        print(adj)
        #print(i*100/n)
        print(city['City'])
        m.add_marker(CircleMarker((float(city['Longitude']), float(city['Latitude'])), '#0036FF', 6))
        for acity in adj:
                
            m.add_marker(CircleMarker((float(acity.info['Longitude']), float(acity.info['Latitude'])), '#0036FF', 6))
            pos1 = (float(city['Longitude']), float(city['Latitude']))
            pos2 = (float(acity.info['Longitude']), float(acity.info['Latitude']))
            m.add_line(Line((pos1, pos2), 'blue', 1))'''
        i = i+1
        '''city = jfile[0]
        m.add_marker(CircleMarker((float(city['Longitude']), float(city['Latitude'])), '#0036FF', 6))
        adj = closeNodes(tree, city, 300)'''
        print()
        for city in other:
            m.add_marker(CircleMarker((float(city['Longitude']), float(city['Latitude'])), '#0036FF', 6))
            #print(city['City'] + " adjacent with ", end='')
            adj = closeNodes(tree, city, 300)
            for acity in adj:
                #print(acity.info['City'], end=' ')
                pos1 = (float(city['Longitude']), float(city['Latitude']))
                pos2 = (float(acity.info['Longitude']), float(acity.info['Latitude']))
                m.add_line(Line((pos1, pos2), 'blue', 1))
            #print()
        '''for acity in adj:
            print(acity.info['City'])
            
            m.add_marker(CircleMarker((float(city['Longitude']), float(city['Latitude'])), '#0036FF', 6))
            pos1 = (float(city['Longitude']), float(city['Latitude']))
            pos2 = (float(acity.info['Longitude']), float(acity.info['Latitude']))
            m.add_line(Line((pos1, pos2), 'blue', 1))'''

        '''for acity in other:
            m.add_marker(CircleMarker((float(acity['Longitude']), float(acity['Latitude'])), '#0036FF', 6))
            for bcity in other:
                if haversine((float(bcity['Longitude']), float(bcity['Latitude'])), (float(acity['Longitude']), float(acity['Latitude']))) <= 300:
                    m.add_marker(CircleMarker((float(bcity['Longitude']), float(bcity['Latitude'])), '#0036FF', 6))
                    pos1 = (float(bcity['Longitude']), float(bcity['Latitude']))
                    pos2 = (float(acity['Longitude']), float(acity['Latitude']))
                    m.add_line(Line((pos1, pos2), 'blue', 1))'''
        end = time.time()
        print("Finished! Time: " + str(end - start))

        image = m.render(zoom=5)
        image.save('map.png')

def printTree(node, file):
    if node != None:
        out = ""
        # f = open(file,'a')
        print("Node " + node.info['City'] + " goes to ", end='')
        if node.left_child is not None:
            print(node.left_child.info['City'] + " and ", end='')
        if node.right_child is not None:
            print(node.right_child.info['City'])
        print()
        if node.left_child is not None:
            # f.write(node.info['City'].replace("-","").replace(" ","") + " -> " + node.left_child.info['City'].replace("-","").replace(" ","") + "\n")
            out = out + (node.info['City'].replace("-", "").replace(" ", "") + node.info['Population'] + " -> " + node.left_child.info[
                'City'].replace("-", "").replace(" ", "")+ node.left_child.info['Population'] + "\n")  + printTree(node.left_child, file)
        if node.right_child is not None:
            # f.write(node.info['City'].replace("-","").replace(" ","") + " -> " + node.right_child.info['City'].replace("-","").replace(" ","") + "\n")
            out = out + (node.info['City'].replace("-", "").replace(" ", "") + node.info['Population']+" -> " + node.right_child.info[
                'City'].replace("-", "").replace(" ", "") +node.right_child.info['Population']+ "\n") + printTree(node.right_child, file)
        # f.close()
        return out


if __name__ == "__main__":
    #generateJSON.processFile("worldcitiespop")
    generateGraph()
