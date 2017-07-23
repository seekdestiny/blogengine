### Project Setup

```
mkdir django_blog

cd django_blog/

git init

virtualenv blogenv --distribute

source blogenv/bin/activate

pip install django

django-admim --version

pip install South

pip install django-toolbelt

pip freeze > requirements.txt

git add requirements.txt

git commit -m "record requirements"

gvim .gitignore

git add .gitignore

git commit -m "add a gitignore file"

django-admin startproject django_blog .

gvim .gitignore

git add .gitignore django_blog/ manage.py

git commit -m "create project skeleton"

python3 manage.py migrate

python3 manage.py runserver

git add django_blog/settings.py history.md

git commit -m "first django-powered page"
```

### Start App

```
python3 manage.py startapp blogengine

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py sqlmigrate blogengine 0001
```

### Creating blog posts via the admin

```
python3 manage.py createsuperuser

mkdir blogengine/fixtures

python3 manage.py dumpdata auth.User --indent=2 > blogengine/fixtures/user.json
```

### Setup Bower and Bootstrap

```
NODE_PATH="/usr/local/lib/node_modules"

sudo npm install -g bower

sudo chown -R $USER:$GROUP ~/.npm

sudo chown -R $USER:$GROUP ~/.config

bower init

bower install bootstrap html5-boilerplate --save

git add .gitignore .bowerrc bower.json

git commit -m 'add bower config'

mkdir templates/blogengine/includes

cp blogengine/static/bower_components/html5-boilerplate/dist/index.html blogengine/templates/blogengine/includes/base.html
```

### Formatting Content

```
pip install markdown2

pip freeze > requirements.txt

mkdir blogengine/templatetags

touch blogengine/templatetags/__init__.py
```

### RSS Feed

```
pip instal feedparser

pip freeze > requirements.txt
```

### Code coverage

```
pip install coverage django-jenkins

pip freeze > requirements.txt

delete with_coverage from django_jenkins.tasks

python3 manage.py jenkins --enable-coverage --coverage-format html

