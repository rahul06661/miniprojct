from http import client
from pymongo import MongoClient

port=27017
ip='localhost'

client= MongoClient(ip,port)

database=client['e-ward' ]


def user_functions(user_obj):
    peoreg_tbl=database['peoreg_tbl']
    peoreg_tbl.insert_one(user_obj)   
    return True
