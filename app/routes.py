from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from app.form import LoginForm, SearchForm
import requests
from flask_login import current_user, login_user, logout_user
from app.models import User
from random import randint

@app.route('/')
def index():
    res = requests.get("http://api.ethanshealey.com/recipes")
    data = res.json()
    return render_template('index.html', title='Cooking', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    banner = 'bg' + str(randint(1,9)) + '.jpg'
    form=SearchForm()
    matches = []
    seen = set()
    if form.validate_on_submit():
        query = form.item.data.split(' ')
        res = requests.get('http://api.ethanshealey.com/recipes')
        data = res.json()
        i = 0
        for recipe in data:
            for q in query:
                if q.lower() in recipe['name']:
                    item = tuple(recipe.items)
                    if item not in seen:
                        seen.add(item)
                        matches.append(recipe)
                        break
                for ing in recipe['ingredients']:
                    if q.lower() in ing:
                        item = tuple(recipe.items)
                        if item not in seen:
                            seen.add(item)
                            matches.append(recipe)
                            break
    '''
    if form.validate_on_submit():
        query = form.item.data.split(' ')
        res = requests.get("http://api.ethanshealey.com/recipes")
        data = res.json()
        counter = 0
        for recipe in data:
            for q in query:
                if q.lower() in recipe['name'].lower():
                    matches.append(recipe)
                    break
    '''

    return render_template('search.html', title='Search', form=form, banner=banner, results=matches)

@app.route('/recipe/<item>/<id>')
def recipe(item, id):
    res = requests.get(f"http://api.ethanshealey.com/recipes/{id}")
    data = res.json()
    banner = 'bg' + str(randint(1,9)) + '.jpg'
    return render_template('recipe.html', title=data['name'], data=data, banner=banner)

@app.route('/recipe/update/<id>')
@login_required
def update(id):
    banner = 'bg' + str(randint(1,9)) + '.jpg'
    res = requests.get(f'http://api.ethanshealey.com/recipes/{id}')
    data = res.json()
    return render_template('update.html', title='Update Recipe', data=data, id=id, banner=banner)


@app.route('/recipe/delete/<id>')
@login_required
def delete(id):
    res = requests.delete(f"http://api.ethanshealey.com/recipes/{id}")
    return redirect(url_for('index'))

@app.route('/upload')
@login_required
def upload():    
    banner = 'bg' + str(randint(1,9)) + '.jpg'
    return render_template('upload.html', title='Add a Recipe', banner=banner)

@app.route('/handle_update/<id>', methods=['GET', 'POST'])
@login_required
def handle_update(id):
    if request.method == 'POST':
        data = request.form
        payload = {'name': '', 'ingredients': [], 'instructions': [], 'cook_time': ''}
        for key,value in data.items():
            if 'name' in key:
                payload['name'] = value.replace("'","''")
            elif 'ingredient' in key:
                payload['ingredients'].append(value.replace("'","''"))
            elif 'instruction' in key:
                payload['instructions'].append(value.replace("'","''"))
            elif 'cook_time' in key:
                payload['cook_time'] = value.replace("'","''")
        res = requests.post(f'http://api.ethanshealey.com/recipes/{id}', json=payload)
    return redirect(url_for('index'))

@app.route('/handle_upload', methods=['GET', 'POST'])
@login_required
def handle_upload():
    if request.method == 'POST':
        data = request.form
        payload = {'name': '', 'ingredients': [], 'instructions': [], 'cook_time': ''}

        for key,value in data.items():
            if 'name' in key:
                payload['name'] = value.replace("'","''")
            elif 'ingredient' in key:
                payload['ingredients'].append(value.replace("'","''"))
            elif 'instruction' in key:
                payload['instructions'].append(value.replace("'","''"))
            elif 'cook_time' in key:
                payload['cook_time'] = value.replace("'","''")

        res = requests.post('http://api.ethanshealey.com/recipes', json=payload)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    banner = 'bg' + str(randint(1,9)) + '.jpg'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form, banner=banner)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
