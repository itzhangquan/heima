from flask import  Flask
from cart import cart

app=Flask(__name__)
app.register_blueprint(cart)

@app.route('/')
def index ():
    return "helloworld"
if __name__ == '__main__':
    print  app.url_map
    app.run(debug=True)