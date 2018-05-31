from flask import  Flask
from product import pro

app=Flask(__name__)
app.register_blueprint(pro)

@app.route('/')
def index ():
    return "helloworld"
if __name__ == '__main__':
    print  app.url_map
    app.run(debug=True)