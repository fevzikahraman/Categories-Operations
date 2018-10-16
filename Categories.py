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


# endpoint to create new category
@app.route("/category", methods=["POST"])
def add_category():
    id = request.json['id']
    name = request.json['name']
    parentCategory = request.json['parentCategory']
    isVisible = request.json['isVisible']

    new_category = Categories(id, name, parentCategory, isVisible)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category)


# endpoint to show all users
@app.route("/categories", methods=["GET"])
def get_user():
    all_categories = Categories.query.all()
    result = category_schema.dump(all_categories)
    return jsonify(result.data)


# endpoint to get category detail by id
@app.route("/category/<id>", methods=["GET"])
def category_detail(id):
    category = Categories.query.get(id)
    return category_schema.jsonify(category)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    category = Categories.query.get(id)
    isVisible = request.json['isVisible']

    category.isVisible = isVisible


    db.session.commit()
    return user_schema.jsonify(category)


# endpoint update visibility
@app.route("/user/<id>", methods=["PATCH"])
def update_visibility(id):
    catetory = Categories.query.get(id)
    db.session.delete(catetory)
    db.session.commit()

    return category_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)