#Importing
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from py_edamam import Edamam
from flask_login import UserMixin
from flask import flash

e = Edamam(recipes_appid='dd3e08d9',
           recipes_appkey='db6b2a58e06f801203d035f5914b6877',
          food_appid='3da38d07',
            food_appkey='2c641685171d1515f82e620028451f69')

#Linking db with Flask /Users/GOD/Desktop/school/447/RecipieFinder/RecipieFinder/RecipieFinder
app = Flask(__name__, template_folder= ".", static_folder='static', static_url_path='/static')
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CMSC447Project_new.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#Initialize the database
db = SQLAlchemy(app)

#All five classes for our data base
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable= False)
    user_password = db.Column(db.String(255))

    def __repr__(self):
        return '<Name %r' %self.user_name

class Recipes(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable= False)
    ingred_array = db.Column(db.String)#ingredients seperate by commas
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
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html')

@app.route('/breakfast', methods= ['POST'])
def breakfast_search():
  search= request.form.get('search')
  recipes= e.search_recipe(search)
  ret= []
  for i in range(len(recipes.get('hits'))):
    name= recipes.get('hits')[i].get('recipe').get('label')
    ingredients= recipes.get('hits')[i].get('recipe').get('ingredients')
    image= recipes.get('hits')[i].get('recipe').get('image')
    ret.append([name, ingredients, image])
  return render_template('/breakfast.html', results= ret)

@app.route('/lunch')
def lunch():
    return render_template('lunch.html')

@app.route('/dinner')
def dinner():
    return render_template('dinner.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/forgot_password', methods=['POST'])
def reset_password():
  if request.method == 'POST':
    email= request.form['email']
    password1= request.form['password1']
    password2= request.form['password2']
    print(f"Email: {email}, Password1: {password1}, Password2: {password2}")
    
    users = User.query.filter_by(user_name = email).all()
    if not users: #email not within database
      flash("Email not in database")
      print("Email not in database")
      return redirect(url_for('signup'))
    
    user = users[0]
    if password1 != password2:
      flash("Passwords do not match")
      print("Passwords do not match")
      return redirect(url_for('forgot_password'))
    #updatepassword
    user.user_password = password1
    db.session.commit()
    
    flash("Password has been reset")
    print("Password has been reset")
  return redirect(url_for('login'))



@app.route('/signup', methods=['POST'])
def signup_submit():
  if request.method == 'POST':
    email= request.form['email']
    password= request.form['password']
    print(f"Email: {email}, Password: {password}")
    
    users= User.query.all()
    for user in users:
      if user.user_name== email:
        print(email)
        print(user.user_name)
        print("User already Exists")
        return redirect(url_for('home'))
      
    print(f"Email: {email}, Password: {password}")
    print("Adding user to database")
    sign_up = User( user_name = email, user_password = password)
    db.session.add(sign_up)
    db.session.commit()
  return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_submit():
  if request.method == 'POST':
    email= request.form['email']
    password= request.form['password']
    print(f"Email: {email}, Password: {password}")

    #user = User.query.filter_by(user_name=email).first()
    #if user: print(true)
    users= User.query.all()
    login= False
    for user in users:
      if user.user_name == email:
         if user.user_password != password:#incorrect password
            print("Username correct but password incorrect")
          
         if user.user_name== email and user.user_password== password:#correct user and password
            print("user found, and password is correct")
            login= True        
            return redirect(url_for('home'))
  #print("User not found")#username not found
  return render_template('login.html')

@app.route('/favorites')
def saved():
  favorites= Favorites.query.all()
  return render_template('/saved', favorites)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
  add_recipe= request.form['favorite']
  user_name= request.form['user']
  recipes= Recipes.query.all()
  favorites= Favorites.query.all()
  users= User.query.all()

  recipe_found= False
  recipe_id= None
  for recipe in recipes:
     if recipe.recipe_name== add_recipe:
        recipe_id= recipe.recipe_id 
        recipe_found = True

  user_id = None
  for user in users:
     if user.user_name== user_name:
        user_id= user.user_id

  if recipe_found== True:
    add_fav= True
    for favorite in favorites:
      if favorite.recipe_id== recipe_id and favorite.user_id== user_id:
        add_fav= False
    if add_fav == True:
      new_favorite= Favorites(user_id= user_id, recipe_id= recipe_id)
      db.session.add(new_favorite)
      db.session.commit()
  return render_template('/saved', favorites)

@app.route('/forgot_password')
def forgot_password():
    return render_template('fpsswd.html')

if __name__== "__main__":
  with app.app_context():
   
    db.create_all()
    # Example of using the Recipes class
    #user= User(user_name= "user1", user_password= "password1")
    #ingredients = ["ingredient1", "ingredient2", "ingredient3"]
   # recipe = Recipes(recipe_name="Example Recipe", time_of_day="Morning")
   # recipe.set_ingredients(ingredients)
    #db.session.add(user)
    #db.session.commit()

  # Retrieving ingredients
  #recipe = Recipes.query.first()
  #ingredients = recipe.get_ingredients()
 # print(ingredients)
  app.run(debug=True)
