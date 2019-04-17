import pyhdb
import json
import sys

"""
sys.argv[1] Database address
sys.argv[2] Port number of the database
sys.argv[3] DB username
sys.argv[4] DB user password
"""
products = [1, 2]


def convert_to_binary_data(productid):
    with open("p" + str(productid) + ".json", 'r') as file:
        json_read = json.load(file)
        json_read["description"] = json_read["description"].replace("'", '$$')
        binary_data = str(json_read).encode('utf8')
        return_tuple = binary_data, (json_read["productId"], json_read["productName"], json_read["description"])

    return return_tuple


serverAddress = sys.argv[1]
serverPort = sys.argv[2]
userName = sys.argv[3]
passWord = sys.argv[4]
conn = pyhdb.connect(serverAddress, serverPort, userName, passWord)

cursor = conn.cursor()
for product in products:
    try:
        return_tuple = convert_to_binary_data(product)
        binary_data = return_tuple[0]

        insert_blob_tuple = (product, binary_data)
        query = "insert into ProductsProp values (:1, :2, :3)"
        ret = cursor.execute(query, return_tuple[1])
        query = "insert into ProductsBlob values (:1, :2)"
        insert_blob_tuple = (product, binary_data)
        ret = cursor.execute(query, insert_blob_tuple)
        conn.commit()
        print("Product {0} Stored".format(product))
    except Exception as msg:
        print(str(msg) + "in ProductId {0}".format(product))
cursor.close()
conn.close()

