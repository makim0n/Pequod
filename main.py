#!/usr/bin/python3

from pequod_docker import *
from pequod_args import *
from pequod_database import *
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
#dic_layer_count = {}
dic_layer_count = {'b4d27d4e4f5bb8bfe5bc92f8b3cbf3f0f5042fe120a40833fc0247deb728f961': 7010, '3b139c8076d9c5ea6935edb9f644a4dd9caec1acb1217b9492fae4bbe3ff3725': 1354, '05f684efc5012328cdbde4e3814eed1240f41d06e4dcb44506705a7705cf199e': 268, 'a934c4c71d618bab83432e24a12640ff9d474df3529fa790cb0f9d059d82c7dd': 6293, 'a67d35ec1f3fd055009a18e40d35ccbbb31da927e5d2c421ec43e98db0d08678': 20819, '34c306ec137d785a0422942d8960b913fa7ff1ec66339b699bb3de02ce6770c6': 24, 'be3d4ffa7682700bcbc51a8655568428c4979c5464169a286208e9e03f7673a5': 17, 'f0e0774e1b8e3c943a4b910e773664c81cfcadda8a388040c842fb37b8a0e467': 5402, 'c03933430e12aa2893ee247934be44c86f5c1878904d7a1bfe665ccd548bde5d': 10, '986a7d85c875d79a1cd37dcd7e4e110cbf6ede072d062dfb0eaf10f006ebefd9': 4, 'b5116739ab4c01c43f0ba2feab4358c367ca86c085fad5223ce03d6bb7933fe3': 4, '5c1926c54c7194b9886f0007f2cfa0a9e166b8985842e55fc9d8e888254663de': 1195, '0425a7cec03536e53ffcd89abeab827ee12987209a0d31085b43cf01b8c8b2cb': 3}

@app.route('/', methods=['GET', 'POST'])
def my_form():
    if request.method == 'POST':
        container = request.form['container']
        select = request.form['getType']
        if container != "":
            if select == "DockerHub":
                username = request.form['dockerhub_username']
                password = request.form['dockerhub_password']
            elif select == "Local":
                pass
            elif select == "Private repository":
                username = request.form['private_username']
                password = request.form['private_password']
                host = request.form['private_host']
                port = request.form['private_port']
            else:
                # No auth docker
                # TODO check if dic_layer_count is empty or not, in order to save time
                with app.app_context():
                    db.create_all()
                    #main_analysis = DockerAnalysis(container, db)
                # for layer in db.session.query(Files.layer).distinct():
                #     tmp = str(layer)[2:-3] # convert sqlalchemy class into str
                #     dic_layer_count[tmp] = db.session.query(Files).filter_by(layer=tmp).count()
                # print(dic_layer_count)
    # TODO find something better to do this
    if not dic_layer_count:
        return render_template('form.html')
    else:
        return render_template('form.html', data=dic_layer_count)

@app.route('/layers')
def parse_layers():
    layer = request.args.get('layer')
    file_meta = {}
    for i in db.session.query(Files).filter_by(layer=layer):
        fname = i.filename
        fsize = i.file_size
        if i.file_content == "NOT A REGULAR FILE":
            ftype = 'd'
        else:
            ftype = 'f'
        file_meta[fname] = [ftype, fsize]
    print(file_meta)
    return render_template('layers.html', layer=layer, file_meta=file_meta, data=dic_layer_count)

if __name__ == "__main__":
    app.run()

    #args = arguments_menu()
    #with app.app_context():
        #db.create_all()
        #main_analysis = DockerAnalysis(args.container, db)

    # rm database.db && python3 app.py
    # curl http://127.0.0.1:5000/items
