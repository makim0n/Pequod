#!/usr/bin/python3

#from pequod_flask import *
from pequod_docker import *
from pequod_args import *
from pequod_database import *
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/items')
def get_item():
    resultqry = db.session.query(Files).all()
    print(resultqry)
    for i in resultqry:
        print(i.owner)
    return "TEMPLATE IS BETTER, LOOK AT YOUR CONSOLE"

if __name__ == "__main__":
    args = arguments_menu()
    with app.app_context():
        db.create_all()
        print(db)
        main_analysis = DockerAnalysis(args.container, db)
    app.run()

    # rm database.db && python3 app.py
    # curl http://127.0.0.1:5000/items
