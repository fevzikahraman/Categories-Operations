from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    parentCategory = db.Column(db.String(120))
    isVisible = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, id, name, parentCategory,isVisible ):
        self.id = id
        self.name = name
        self.parentCategory = parentCategory
        self.isVisible = isVisible


class CategorySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name','parentCategory', 'isVisible')


category_schema = CategorySchema()
category_schema_schema = CategorySchema(many=True)




if __name__ == '__main__':
    app.run(debug=True)