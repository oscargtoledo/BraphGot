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


class Node(namedtuple('Node', 'city population location left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))



earthRadius = 6371000
def kdtree(point_list, depth=0):
    if not point_list:
        return None

    #k = len(point_list[0])  # assumes all points have the same dimension
    k = 2
    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k

    # Sort point list by axis and choose median as pivot element
    #point_list.sort(key=itemgetter(axis))
    if(axis==0):
        point_list.sort(key=lambda x: float(earthRadius)*float(x['Longitude']))
    else:
        point_list.sort(key=lambda x: float(earthRadius)*float(x['Latitude']))
    median = len(point_list) // 2

    # Create node and construct subtrees
    return Node(
        location=(point_list[median]['Latitude'],point_list[median]['Longitude']),
        city=point_list[median]['City'],
        population=point_list[median]['Population'],
        left_child=kdtree(point_list[:median], depth + 1),
        right_child=kdtree(point_list[median + 1:], depth + 1)
    )

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
        print(sorted(jfile,key=lambda x: float(x['Latitude'])))


        tree = kdtree(jfile)


        m = StaticMap(2000, 2000, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
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
        image.save('map.png')



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
    treeTest()
    #jsonTesting()
    #jsonTesting()

    #print(fuzz.ratio("Andorra la Vella","Andorra-Vieille"))

