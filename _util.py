import _product as pp
import _objects as obj
import sqlalchemy as db
import json
import os
import logging
import traceback
#from hdbcli import dbapi
#import pyhdb


def convert_to_json_data(binary_data):
    return binary_data.decode('utf-8').replace("\'", '"').replace("$$", "'")



def get_connectionPostgres():
    if obj.conn is not None and obj.conn.isconnected():
        obj.conn.close()
        db.create_engine()
    uri = json.loads(os.getenv('VCAP_SERVICES'))['postgresql'][0]['credentials']['uri']
    logging.info('Using postgres credentials from VCAP_SERVICES: ' + uri)
    obj.data = db
    obj.engine = obj.data.create_engine(uri)
    obj.conn = obj.engine.connect()


def get_connectionHana():
    if obj.conn is not None and obj.conn.isconnected():
        obj.conn.close()
        db.create_engine()
    #obj.conn = dbapi.connect(serverAddress, serverPort, userName, passWord)
    #uri = json.loads(os.getenv('VCAP_SERVICES'))['hana'][0]['credentials']['uri']
    #uri = json.loads(os.getenv('VCAP_SERVICES'))['hanatrial'][0]['credentials']['url']
    host = json.loads(os.getenv('VCAP_SERVICES'))['hanatrial'][0]['credentials']['host']
    port = json.loads(os.getenv('VCAP_SERVICES'))['hanatrial'][0]['credentials']['port']
    usesr = json.loads(os.getenv('VCAP_SERVICES'))['hanatrial'][0]['credentials']['user']
    password = json.loads(os.getenv('VCAP_SERVICES'))['hanatrial'][0]['credentials']['password']
    schema = json.loads(os.getenv('VCAP_SERVICES'))['hanatrial'][0]['credentials']['schema']
    uri = 'hana://' + usesr + ':' + password + '@' + host + ':' + str(port) + '/?currentschema=' + schema
    logging.info('Using hana credentials from VCAP_SERVICES: ' + uri)

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
    name_filter = " lower(Products." + '"ProductName")' + " ~ lower('{0}')".format(
        product_name if product_name is not None else "")
    description_filter = " and lower(Products." + '"Description")' + " ~ lower('{0}')".format(
        product_description if product_description is not None else "")
    id_filter = "and Products." + '"ProductId"' + " = {0}".format(id_valid) if id_valid is not None else ""
    query = str("select * from Products where {0} {1} {2}".format(name_filter, description_filter, id_filter))
    #query = "select * from Products"
    try:
        ret = obj.conn.execute(query).fetchall()
        for row in ret:
            #json_object = json.loads(row[3])
            json_object = row[3]
            pp.Product(json_object)
    except Exception as msg:
        logging.info(traceback.format_exc())
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
