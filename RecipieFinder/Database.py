#Importing
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_required
#from sqlalchemy.orm import relationship
import requests
import re

#Linking db with Flask /Users/GOD/Desktop/school/447/RecipieFinder/RecipieFinder/RecipieFinder
app = Flask(__name__, template_folder= ".", static_folder='static', static_url_path='/static')
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CMSC447Project_new5.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#Initialize the database
db = SQLAlchemy(app)

def get_recipe_id(url):
    # Use regular expression to extract the id after "recipe_"
    match = re.search(r'recipe_(\w+)$', url)
    recipe_id = match.group(1)
    return recipe_id

def find_recipes(id):
    # API endpoint URL
    url = "https://api.edamam.com/api/recipes/v2/"
    url+= id
    # API credentials
    app_id = "dd3e08d9"
    app_key = "db6b2a58e06f801203d035f5914b6877"

    # Search parameters
    params = {
        "type": "public",
        "app_id": app_id,
        "app_key": app_key,
    }

    # Make the API request
    response = requests.get(url, params=params)
    recipes = response.json()
    return recipes

def get_recipes(query, cuisineType= None, mealType= None, dishType=None, diet= None, health= None, random= False):
    # API endpoint URL
    url = "https://api.edamam.com/api/recipes/v2"

    # API credentials
    app_id = "4e1c4b9e"
    app_key = "c07ac735f49f7a715321d4fe7f5e71de"

    # Search parameters
    params = {
        "type": "public",
        "app_id": app_id,
        "app_key": app_key,
        "mealType": mealType,
        "dishType": dishType,
        'diet': diet,
        'health': health,
        'cuisineType': cuisineType,
        'random': random,
        'q': query
    }

    # Make the API request
    response = requests.get(url, params=params)
    print(url, params)
    recipes=[]
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response data (e.g., convert to JSON, print results)
        recipes = response.json()
        for i in range(len(recipes.get('hits'))):
            name= recipes.get('hits')[i].get('recipe').get('label')
            ingredients= recipes.get('hits')[i].get('recipe').get('ingredients')
            image= recipes.get('hits')[i].get('recipe').get('image')
            print(name)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
    return recipes

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
    #ingred_array = db.Column(db.String)#ingredients seperate by commas
    time_of_day = db.Column(db.String(50), nullable= False)
    
    def __repr__(self):
        return '<Name %r' %self.recipe_name

    #def __repr__(self):
    #  return f'<Recipe {self.recipe_name}>'

   # def set_ingredients(self, ingredients):
    #  self.ingred_array = json.dumps(ingredients)

  #  def get_ingredients(self):
  #    return json.loads(self.ingred_array) if self.ingred_array else []

class login_status(db.Model):
    id = db.Column(db.Integer, primary_key=True)# Define a primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    login= db.Column(db.Boolean, nullable= False)

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)# Define a primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    recipe_name =  db.Column(db.Integer, db.ForeignKey('recipes.recipe_name'))
    # fav_ingred_array = db.Column(db.String)#ingredients seperated by commas
    def __repr__(self):
      return f"Favorites(user_id={self.user_id},recipe_name= {self.recipe_name})"
    
@app.route('/')
def home():
    login = session.get('login', False)
    user= session.get('user', None)
    return render_template('index.html', login= login)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/breakfast')
def breakfast():
    login = session.get('login', False)
    user= session.get('user', None)
    return render_template('breakfast.html')

@app.route('/search', methods= ['POST'])
def Search():
  search= request.form.get('search')
  cuisinetype= request.form.get('cuisineType')
  mealType = request.form.get('mealType')

  if cuisinetype== "None":
    cuisinetype= None
  if mealType== "None":
     mealType= None

  recipes= get_recipes(search, cuisineType= cuisinetype, mealType= mealType)
  ret= []
  for i in range(len(recipes.get('hits'))):
    name= recipes.get('hits')[i].get('recipe').get('label')
    ingredients= recipes.get('hits')[i].get('recipe').get('ingredients')
    image= recipes.get('hits')[i].get('recipe').get('image')
    id= get_recipe_id(recipes.get('hits')[i].get('recipe').get('uri'))
    ret.append([name, ingredients, image, id])
    print(id)
  login = session.get('login', False)
  user= session.get('user', None)
  return render_template('/search.html', results= ret, login = login, user = user)

@app.route('/breakfast', methods= ['POST'])
def breakfast_search():
  search= request.form.get('search')
  cuisinetype= request.form.get('cuisineType')
  mealType = request.form.get('mealType')

  if cuisinetype== "None":
    cuisinetype= None
  if mealType== "None":
     mealType= None

  recipes= get_recipes(search, cuisineType= cuisinetype, mealType= mealType)
  ret= []
  for i in range(len(recipes.get('hits'))):
    name= recipes.get('hits')[i].get('recipe').get('label')
    ingredients= recipes.get('hits')[i].get('recipe').get('ingredients')
    image= recipes.get('hits')[i].get('recipe').get('image')
    id= get_recipe_id(recipes.get('hits')[i].get('recipe').get('uri'))
    ret.append([name, ingredients, image, id])
    print(id)
  login = session.get('login', False)
  user= session.get('user', None)
  return render_template('/breakfast.html', results= ret, login = login, user = user)


@app.route('/recipe_detail/<string:recipe_name>')
def recipe_detail(recipe_id):
  print(recipe_id)
    # Fetch recipe details based on recipe_name from the database or API
    # For now, let's pass a placeholder dictionary as an example
  print("This is ", recipe_id)
  recipe = find_recipes(recipe_id)
  name= recipe.get('recipe').get('label')
  ingredients= recipe.get('recipe').get('ingredients')
  image= recipe.get('recipe').get('image')
  calories= recipe.get('recipe').get('calories')
  mealType=recipe.get('recipe').get('mealType')
  dishType= recipe.get('recipe').get('dishType')
  dietLabels= recipe.get('recipe').get('dietLabels')
  healthLabels= recipe.get('recipe').get('healthLabels')
  url=  recipe.get('recipe').get('url')

  recipe_details = {
    'recipe_name': name,
    'ingredients': ingredients,
    'image': image,
    'calories': calories,
    'mealType': mealType,
    'dishType': dishType,
    'dietLabels': dietLabels,
    'healthLabels': healthLabels,
    'url': url
  }
  return render_template('recipe_detail.html', recipe=recipe_details)

@app.route('/lunch')
def lunch():
    return render_template('lunch.html')

@app.route('/dinner')
def dinner():
    return render_template('dinner.html')


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('home'))

@app.route('/search', methods=['POST'])
def Save_favorite():
   print("Button click")
   if request.method == 'POST':
      recipe_name = request.form['recipe_name']
      user_name = session.get('user')
      ingredients = request.form['ingredients']
      time_of_day = request.form['time_of_day'] 
      print(f"Username: {user_name}, recipe_name: {recipe_name}")

      if not (recipe_name and user_name and ingredients and time_of_day):
        return jsonify({'error': 'Missing required data'}), 400

      user = User.query.filter_by(user_name = user_name).first()

      if user:
        #  recipe =Recipes(
        #     recipe_name = recipe_name,
        #     time_of_day = time_of_day,
        #  )
        #  recipe.set_ingredients(json.loads(ingredients))

        #  db.session.add(recipe)

         favorite = Favorites(user_id=user.user_id, recipe_name = recipe_name)

         db.session.add(favorite)
         db.session.commit()

         print(f"Recipe '{recipe_name}' saved as a favorite for {user_name}!")
         
      return redirect(url_for('favorites'))


@app.route('/favorites', methods=['POST'])
def Remove_favorite():
    fav_name = request.form['favorite_id']
    favorite_to_remove = Favorites.query.filter_by(recipe_name=fav_name).first()

    if favorite_to_remove:
        db.session.delete(favorite_to_remove)
        db.session.commit()
        print("Item has been successfully removed")
    else:
        print("Favorite not found")

    return redirect(url_for('saved'))


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
            session['login']= True
            session['user'] = user.user_name
            login = session.get('login')
            user= session.get('user')   
            return render_template('favorites.html', login= login)
  print("User not found")#username not found
  session['login']= False
  session['user']= None
  return render_template('login.html')

@app.route('/favorites')
def saved():
 
  # fav1 = Favorites(user_id= 1, recipe_name = "Scrambled eggs")
  # db.session.add(fav1)
  # db.session.commit()
  
  # fav2 = Favorites(user_id= 1, recipe_name = "steak")
  # db.session.add(fav2)
  # db.session.commit()

  # fav3 = Favorites(user_id= 2, recipe_name = "Pork")
  # db.session.add(fav3)
  # db.session.commit()
  #fav = Favorites.query.filter_by(user_id= testid).all()
  users= User.query.all()
  Uid = -1
  login= False
  for user in users:
    if user.user_name == session['user']:
       Uid = user.user_id
  print(f"Uid:{Uid}")
  fav= Favorites.query.all()
  results = []
  for favor in fav:
     if favor.user_id ==  Uid:
        results.append(favor)


  print("fav")
  print(f"{results}")
  return render_template('favorites.html', favorites= results)


# @app.route('/add_favorite', methods=['POST'])
# def add_favorite():
#   add_recipe= request.form['favorite']
#   user_name= request.form['user']
#   recipes= Recipes.query.all()
#   favorites= Favorites.query.all()
#   users= User.query.all()

#   recipe_found= False
#   recipe_id= None
#   for recipe in recipes:
#      if recipe.recipe_name== add_recipe:
#         recipe_id= recipe.recipe_id 
#         recipe_found = True

#   user_id = None
#   for user in users:
#      if user.user_name== user_name:
#         user_id= user.user_id

#   if recipe_found== True:
#     add_fav= True
#     for favorite in favorites:
#       if favorite.recipe_id== recipe_id and favorite.user_id== user_id:
#         add_fav= False
#     if add_fav == True:
#       new_favorite= Favorites(user_id= user_id, recipe_id= recipe_id)
#       db.session.add(new_favorite)
#       db.session.commit()
#   return render_template('/saved', favorites)

@app.route('/forgot_password')
def forgot_password():
    return render_template('fpsswd.html')

if __name__== "__main__":
  with app.app_context():
   
    db.create_all()
  app.run(debug=True)
