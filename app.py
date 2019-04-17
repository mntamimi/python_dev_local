from flask import Flask, redirect, url_for, request, render_template
import controllers.product as pp
import controllers.objects as obj
import json
import os


#__templates = "templates"
#serverAddress = str(sys.argv[1]) #"localhost"
#serverPort = int(sys.argv[2]) #30015
pp.products.clear()
products = []
app = Flask(__name__, static_url_path='', static_folder='static')
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "5000"))
debug = True if int(os.getenv("DEBUG", '0'))==1 else False


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    jsonresponce = {"Message": "Authentication failed!", "ProductPage": ""}
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        try:
            util.get_connection()
            obj.connected = True
            jsonresponce["Message"] = ""
            jsonresponce["ProductPage"] = render_template("products.html")
        except Exception as msg:
            if obj.conn is not None: #and obj.conn.isconnected():
                obj.conn.close()
            obj.conn = None
            obj.connected = False
            jsonresponce["Message"] = msg.strerror
        finally:
            return json.dumps(jsonresponce, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    return render_template("login.html")


@app.route("/products", methods=["GET", "POST"])
def products_page():
    if obj.conn is None: #or not obj.conn.isconnected():
        return redirect(url_for("login"))
    if request.method == "POST":
        pp.products.clear()
        product_id_filter = request.form.get("ProductId", "")
        product_name_filter = request.form.get("ProductName", "")
        product_description_filter = request.form.get("ProductIdDesc", "")
        util.read_product(product_id=product_id_filter, product_name=product_name_filter,
                          product_description=product_description_filter)
        main_result = {"products": pp.products}
        return json.dumps(main_result, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    return render_template("products.html")


if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug)
    #port = int(sys.argv[4])
    #app.run(host=str(sys.argv[3]), port=port)
    #app.run(debug=True)