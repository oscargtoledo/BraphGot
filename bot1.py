#!/usr/bin/python3

# importa l'API de Telegram
import telegram
import staticmap
from staticmap import StaticMap, Line, CircleMarker

import generateJSON
import json
from telegram.ext import Updater
from telegram.ext import CommandHandler
import networkx as nx
from collections import namedtuple
from operator import itemgetter
from pprint import pformat
from haversine import haversine, Unit
import math
import time


#from fuzzywuzzy import fuzz


class Tree(object):
    def __init__(self, name='root',children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    def print(self):
        print(self.name,end=' ')
        for child in self.children:
            child.print()



class Node(namedtuple('Node', 'city population location latlon left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))




appGraph = None
nodeTree = None

earthRadius = 6371000
def kdtree(point_list, depth=0):
    if not point_list:
        return None

    #k = len(point_list[0])  # assumes all points have the same dimension
    k = 3
    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k

    # Sort point list by axis and choose median as pivot element
    #point_list.sort(key=itemgetter(axis))

    #x = cos(lat)*cos(lon)
    #y = cos(lat)*sin(lon)
    #z = sin(lat)
    if(axis==0):
        point_list.sort(key=lambda x: math.cos(float(x['Latitude'])) * math.cos(float(x['Longitude'])))
    elif(axis==1):
        point_list.sort(key=lambda x: math.cos(float(x['Latitude'])) * math.cos(float(x['Longitude'])))
    else:
        point_list.sort(key=lambda x: math.sin(float(x['Latitude'])))
    median = len(point_list) // 2

    x = math.cos(float(point_list[median]['Latitude'])) * math.cos(float(point_list[median]['Longitude']))
    y = math.cos(float(point_list[median]['Latitude'])) * math.sin(float(point_list[median]['Longitude']))
    z = math.sin(float(point_list[median]['Latitude']))
    # Create node and construct subtrees
    return Node(
        location=(x,y,z),
        latlon=(float(point_list[median]['Latitude']),float(point_list[median]['Longitude'])),
        city=point_list[median]['City'],
        population=point_list[median]['Population'],
        left_child=kdtree(point_list[:median], depth + 1),
        right_child=kdtree(point_list[median + 1:], depth + 1)
    )
def dist(pos1,pos2):
    return math.sqrt(math.pow(pos2[0]-pos1[0],2)+math.pow(pos2[1]-pos1[1],2)+math.pow(pos2[2]-pos1[2],2))

def closeNodes(root, node, latlon, distance, depth=0):
    outList = []
    k = 3
    axis = depth % k
    if(root is None):
        return outList
    else:
        if(root.location[axis]<node[axis]):
            outList.extend(closeNodes(root.left_child,node,latlon,distance))
            if(root.location[axis]-node[axis] < distance):
                outList.extend(closeNodes(root.right_child,node,latlon,distance))
        elif(root.location[axis]>node[axis]):
            outList.extend(closeNodes(root.right_child,node,latlon,distance))
            if(root.location[axis]-node[axis] < distance):
                outList.extend(closeNodes(root.left_child,node,latlon,distance))
        else: 
            pass

        if(haversine(root.latlon,latlon)<=distance):
            outList.append(root)
            





        '''if (dist(root.location,node) <= distance):
            outList.append(root)
            if(root.left_child is not None and dist(root.left_child.location, node) <= distance):
                #outList = outList ++ root.left_child ++ closeNodes(root.left_child, node, distance)
                outList.append(root.left_child)
                outList.extend(closeNodes(root.left_child,node,distance))
            if(root.right_child is not None and dist(root.right_child.location, node) <= distance):
                #outList = outList ++ root.right_child ++ closeNodes(root.right_child, node, distance)
                outList.append(root.right_child)
                outList.extend(closeNodes(root.right_child,node,distance))'''
    return outList



def treeTest():
    '''t = Tree('*', [Tree('1'),
               Tree('2'),
               Tree('+', [Tree('3'),
                          Tree('4')])])
    t.print()'''
    #kde-tree
    #point_list = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    #tree = kdtree(point_list)
    #print(tree)
    with open('worldcitiespop.json', 'r', encoding="utf8") as json_file:
        jfile = json.load(json_file)
        #print(sorted(jfile,key=lambda x: float(x['Latitude'])))
        G = nx.Graph()
        m = StaticMap(2000, 2000, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

        for city in jfile:
            if(float(city['Population'])>=3000):
                jfile.remove(city)
            else: 
                G.add_node(city['City'])
                latlon = (float(city['Latitude']),float(city['Longitude']))
                m.add_marker(CircleMarker((latlon[1],latlon[0]),'#0036FF',6))
                #tree = kdtree(jfile)
                image = m.render(zoom=5)
                image.save('map.png')

        
        
        '''for city in jfile:
            cityPosition = (math.cos(float(city['Latitude'])) * math.cos(float(city['Longitude'])),math.cos(float(city['Latitude'])) * math.sin(float(city['Longitude'])) , math.sin(float(city['Latitude'])) )
            closeByNodes = closeNodes(tree,cityPosition,latLon,200)
            for closeCity in closeNodes:

'''




        '''m = StaticMap(2000, 2000, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
        for city in jfile:
            if(float(city['Population'])>100000):
                print(city['City'])
                lon = float(city['Longitude'])
                lat = float(city['Latitude'])
                marker_outline = CircleMarker((lon, lat), 'white', 6)
                marker = CircleMarker((lon, lat), '#0036FF', 6)

                m.add_marker(marker_outline)
                m.add_marker(marker)




        image = m.render(zoom=5)
        image.save('map.png')'''
def latLonToCoord(latlon):
    x = math.cos(float(latlon[0])) * math.cos(float(latlon[1]))
    y = math.cos(float(latlon[0])) * math.sin(float(latlon[1]))
    z = math.sin(float(latlon[0]))
    return (x,y,z)

#citiesJson = None
def initGraph(bot, update, args):
    start = time.time()
    print("Distance = " + str(args[0]) + " Population = " + str(args[1]))
    with open('worldcitiespop.json', 'r', encoding="utf8") as json_file:
        m = StaticMap(9000,3000,url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
        #print(sorted(jfile,key=lambda x: float(x['Latitude'])))
        jfile = json.load(json_file)
        #appGraph = nx.Graph()
        other = []
        for city in jfile:
            #print(city['City'])
            if(float(city['Population'])>=args[1]):
                #jfile.remove(city)
                other.append(city)

        done = set()


        tree = kdtree(other)
        appGraph = nx.Graph()
        t = 0
        c = 0
        for city in other:
            done.add(city['City'])
            #print(city['City'])
            #appGraph.add_node(city['City'])
            latlon = (float(city['Latitude']),float(city['Longitude']))
            m.add_marker(CircleMarker((latlon[1],latlon[0]),'#0036FF',6))
            #ns = time.time()
            nearCities = closeNodes(tree, latLonToCoord(latlon), latlon, args[0])
            #c = c+1
            #t = t + time.time()-ns
            #print("Cities processed: " + str(c) + " Average time taken: " + str(t/c))
            appGraph.add_node(city['City'])
            for nearCity in nearCities:
            #    pass
                m.add_marker(CircleMarker((nearCity.latlon[1], nearCity.latlon[0]), 'red', 6))
                m.add_line(Line(((latlon[1], latlon[0]), (nearCity.latlon[1], nearCity.latlon[0])), 'blue', 1))
                appGraph.add_node(nearCity.city)
                appGraph.add_edge(city['City'],nearCity.city)


        '''print(jfile[0]['City'])
        # appGraph.add_node(city['City'])
        latlon = (float(jfile[0]['Latitude']), float(jfile[0]['Longitude']))
        m.add_marker(CircleMarker((latlon[1],latlon[0]),'#0036FF',6))
        nearCities = closeNodes(tree, latLonToCoord(latlon), latlon, args[0])
        appGraph.add_node(city['City'])
        for nearCity in nearCities:
            appGraph.add_node(nearCity.city)
            m.add_marker(CircleMarker((nearCity.latlon[1], nearCity.latlon[0]), '#0036FF', 6))
            appGraph.add_edge(jfile[0]['City'], nearCity.city)
            m.add_line(Line(((latlon[1], latlon[0]), (nearCity.latlon[1], nearCity.latlon[0])), 'blue', 3))'''

        end = time.time()
        print("Finished! Time: " + str(end-start))
        image = m.render(zoom=5)
        image.save('map.png')
        #nodeTree = kdtree(jfile)

def plotPop(bot, update, args):
    if(args[2] != None):
        queryPos = (args[1],args[2])
        closeCities = closeNodes(nodeTree,latLonToCoord(queryPos),queryPos,args[0])
        for city in closeCities:
            popMap = appGraph


    else:
        pass
        #query user position

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola! Soc un bot bàsic.")

def main():
    # declara una constant amb el access token que llegeix de token.txt
    TOKEN = open('token.txt').read().strip()

    # crea objectes per treballar amb Telegram
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # indica que quan el bot rebi la comanda /start s'executi la funció start
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('gt', jsonTesting, pass_args=True))
    dispatcher.add_handler(CommandHandler('graph', initGraph, pass_args=True))
    dispatcher.add_handler(CommandHandler('plotpop', plotPop, pass_args=True))


    # engega el bot
    updater.start_polling()

def jsonTesting(bot, update, args):
    #generateJSON.processFile('worldcitiespop')
    with open('worldcitiespop.json', 'r', encoding="utf8") as json_file:
        test = json.load(json_file)
        # print(test)
        print("neter")
        graphTest(test,bot,update,args)
        # for key in test.keys():
        #     print(key)
        #     for city in test.get(key):
        #         for key2 in city.keys():
        #             print(city.get(key2),end=' ')
        #         print()
        #     print()

def graphTest(file,bot,update,args):

    G = nx.Graph()
    try:
        distancia = float(args[0])
        poblacio = float(args[1])
        print("Distancia: " + str(distancia) + " Població: " + str(poblacio))
        for key in file.keys():
            #print(key)
            for city in file.get(key):
                print(city['City'])
                G.add_node(city['City'])
            print()
        bot.send_message(chat_id=update.message.chat_id, text="Dibuixant graf")
        nx.draw(G, with_labels=True,font_weight='bold')
        bot.send_message(chat_id=update.message.chat_id, text="Graf dibuixat")
    except Exception as e:
        print(e)


if __name__=="__main__":
    #main()
    #generateJSON.processFile('worldcitiespop')
    #treeTest()
    initGraph(None,None,[300,100000])
    #jsonTesting()
    #jsonTesting()

    #print(fuzz.ratio("Andorra la Vella","Andorra-Vieille"))

