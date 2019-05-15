#!/usr/bin/python3

# importa l'API de Telegram
import telegram
import generateJSON
import json
from telegram.ext import Updater
from telegram.ext import CommandHandler
import networkx as nx
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



def treeTest():
    t = Tree('*', [Tree('1'),
               Tree('2'),
               Tree('+', [Tree('3'),
                          Tree('4')])])
    t.print()
    #kde-tree
    with open('worldcitiespop.json', 'r', encoding="utf8") as json_file:
        jfile = json.load(json_file)




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
    treeTest()
    #generateJSON.processFile('worldcitiespop')
    #jsonTesting()
    #jsonTesting()

    #print(fuzz.ratio("Andorra la Vella","Andorra-Vieille"))

