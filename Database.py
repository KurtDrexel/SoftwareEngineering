#Importing
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Linking db with Flask
app = Flask(__name__, template_folder= "/home/runner/CMSC447-Pro")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CMSC447Project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#Initialize the database
db = SQLAlchemy(app)

#All five classes for our data base
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable= False)
    user_password= db.Column(db.Integer)

    def __repr__(self):
        return '<Name %r' %self.user_name

class Recipes(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable= False)
    ingred_array = db.Column(db.String)#ingredients seperate by commas
    ##instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.instructor_id'))
    time_of_day = db.Column(db.String(50), nullable= False)
    
    def __repr__(self):
        return '<Name %r' %self.recipe_name

    #def __repr__(self):
    #  return f'<Recipe {self.recipe_name}>'

    def set_ingredients(self, ingredients):
      self.ingred_array = json.dumps(ingredients)

    def get_ingredients(self):
      return json.loads(self.ingred_array) if self.ingred_array else []



class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)# Define a primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    fav_ingred_array = db.Column(db.String)#ingredients seperated by commas
    def __repr__(self):
      return (self.recipe_id)


if __name__== "__main__":
  with app.app_context():
    db.create_all()
    # Example of using the Recipes class
    user= User(user_name= "user1", user_password= "password1")
    ingredients = ["ingredient1", "ingredient2", "ingredient3"]
    recipe = Recipes(recipe_name="Example Recipe", time_of_day="Morning")
    recipe.set_ingredients(ingredients)
    db.session.add(recipe)
    db.session.commit()

  # Retrieving ingredients
  #recipe = Recipes.query.first()
  #ingredients = recipe.get_ingredients()
 # print(ingredients)
  app.run(debug=True)
