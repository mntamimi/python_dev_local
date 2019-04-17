from controllers import product as pp, objects as obj
import sqlalchemy as db
import json
import os
import logging
#from hdbcli import dbapi
#import pyhdb


def convert_to_json_data(binary_data):
    return binary_data.decode('utf-8').replace("\'", '"').replace("$$", "'")


def get_connection():
    if obj.conn is not None and obj.conn.isconnected():
        obj.conn.close()
        db.create_engine()
    #obj.conn = dbapi.connect(serverAddress, serverPort, userName, passWord)
    uri = json.loads(os.getenv('VCAP_SERVICES'))['hana'][0]['credentials']['uri']
    logging.info('Using postgres credentials from VCAP_SERVICES: ' + uri)

    #url = 'hana://' + userName + ':' + passWord + '@' + serverAddress + ':' + str(serverPort)
    obj.data = db
    obj.engine = obj.data.create_engine(uri)
    obj.conn = obj.engine.connect()
    #obj.metadata = obj.data.MetaData()
    #obj.conn = pyhdb.connect(serverAddress, serverPort, userName, passWord)

def get_connectionOld(serverAddress, serverPort, userName, passWord):
    if obj.conn is not None and obj.conn.isconnected():
        obj.conn.close()
        db.create_engine()
    #obj.conn = dbapi.connect(serverAddress, serverPort, userName, passWord)
    uri = json.loads(os.getenv('VCAP_SERVICES'))['postgresql'][0]['credentials']['uri']
    logging.info('Using postgres credentials from VCAP_SERVICES: ' + uri)

    url = 'hana://' + userName + ':' + passWord + '@' + serverAddress + ':' + str(serverPort)
    obj.data = db
    obj.engine = obj.data.create_engine(uri)
    obj.conn = obj.engine.connect()
    #obj.metadata = obj.data.MetaData()
    #obj.conn = pyhdb.connect(serverAddress, serverPort, userName, passWord)


def read_product(product_id=None, product_name=None, product_description=None):
    id_valid = product_id
    if product_id is not None:
        try:
            id_valid = int(product_id)
        except ValueError:
            id_valid = None
    name_filter = " LOWER(productname) like LOWER('%{0}%')".format(product_name if product_name is not None else "")
    description_filter = " and LOWER(description) like LOWER('%{0}%')".format(
        product_description if product_description is not None else "")
    id_filter = "and productid = {0}".format(id_valid) if id_valid is not None else ""
    query = "select * from products where {0} {1} {2}".format(name_filter, description_filter, id_filter)
    try:
        ret = obj.conn.execute(query).fetchall()
        for row in ret:
            json_object = json.loads(convert_to_json_data(row[3].obj))
            pp.Product(json_object)
    except Exception as msg:
        raise msg
"""
    cursor = obj.conn.cursor()
    try:
        cursor.execute(query)
        ret = cursor.fetchall()
        for row in ret:
            json_object = json.loads(convert_to_json_data(row[3].obj))
            pp.Product(json_object)
    except Exception as msg:
        raise msg
    finally:
        cursor.close()
"""
