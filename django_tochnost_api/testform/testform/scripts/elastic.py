import MySQLdb
import json
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index, Document, Text
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import requests
import json




def get_dadata_all():
    db = MySQLdb.connect(passwd="mypass", db="dadata", user='graphtest', charset="utf8mb4", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("SELECT `id`,`inn`,`name`,`ogrn`,`region` FROM `dadata`;")
    cont = []
    for name in cursor.fetchall():
        cont.append({
            'id':name[0],
            'inn':name[1],
            'name': name[2],
            'ogrn': name[3],
            'region': name[4],
        })
    cursor.close()
    return cont

class Dadata(Document):
    inn = Text()
    name = Text()
    ogrn = Text()
    region = Text()

    class Index:
        name = 'dadata'
        settings = {
          "number_of_shards": 2,
        }

    class Meta:
        # name of index. Will be used in search
        index = 'dadata'

def insert_all():
    connections.create_connection(hosts=['localhost'])
    Dadata.init()

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    # connections.create_connection()
    # es = connections.get_connection()
    # es.indices.create(index='dadata')

    counter = 0
    for item in get_dadata_all()[0:100]:
        counter+=1
        obj = Dadata(
            meta={
                'id': item['id']
            },
            inn=str(item['inn']),
            name=str(item['name']),
            orgn=str(item['ogrn']),
            region=str(item['region'])
        )
        obj.save()

        # url = 'http://localhost:9200/dadata/entries/'+str(counter)
        # res = requests.post(url,headers=headers,data=json.dumps(item))



    print('Completed')
