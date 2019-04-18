from flask import Flask, redirect, url_for, request, render_template
import _product
import _util
import _objects
import json
import os
import logging
from flask_debugtoolbar import DebugToolbarExtension
import uuid


#__templates = "templates"
#serverAddress = str(sys.argv[1]) #"localhost"
#serverPort = int(sys.argv[2]) #30015
#_product.products.clear()
products = []
app = Flask(__name__, static_url_path='', static_folder='static')
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "5000"))
debug = True if int(os.getenv("DEBUG", '0'))==1 else False

instance = str(os.getenv("CF_INSTANCE_INDEX", 0))
vcap_application = json.loads(os.getenv('VCAP_APPLICATION'))
cf_app = dict(name=vcap_application['application_name'], uri=vcap_application['application_uris'], port=port)

# the toolbar is only enabled in debug mode:
app.debug = debug
app.config['SECRET_KEY'] = str(uuid.uuid4())
toolbar = DebugToolbarExtension(app)

logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    jsonresponce = {"Message": "Authentication failed!", "ProductPage": ""}
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        try:
            _util.get_connectionPostgres()
            _objects.connected = True
            jsonresponce["Message"] = ""
            jsonresponce["ProductPage"] = ""
        except Exception as msg:
            if _objects.conn is not None: #and _objects.conn.isconnected():
                _objects.conn.close()
            _objects.conn = None
            _objects.connected = False
            jsonresponce["Message"] = msg.strerror
            logging.info(msg.strerror)
        finally:
            return json.dumps(jsonresponce, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    return render_template("login.html")


@app.route("/products", methods=["GET", "POST"])
def products_page():
    if _objects.conn is None: #or not _objects.conn.isconnected():
        return redirect(url_for("login"))
    if request.method == "POST":
        _product.products.clear()
        product_id_filter = request.form.get("ProductId", "")
        product_name_filter = request.form.get("ProductName", "")
        product_description_filter = request.form.get("ProductIdDesc", "")
        _util.read_product(product_id=product_id_filter, product_name=product_name_filter,
                           product_description=product_description_filter)
        main_result = {"products": _product.products}
        return json.dumps(main_result, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    return render_template("products.html")


if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug)
    #port = int(sys.argv[4])
    #app.run(host=str(sys.argv[3]), port=port)
    #app.run(debug=True)