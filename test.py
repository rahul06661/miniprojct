from ipaddress import ip_address
from pymongo import MongoClient
import datetime


#sudo systemctl start mongod

ip_address='localhost'
port=27017

client = MongoClient('localhost', 27017)



if 'e-pancahyath' not in client.list_database_names():
    db = client['e-pancahyath']
else:
    db =client['e-pancahyath']

user_table=db['user_table']
user_table3=db['user_table3']
user_tabl4=db['user_table4']



post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

posts = user_table
post_id = posts.insert_one(post)
post1=user_table3
post1.insert_one(post)