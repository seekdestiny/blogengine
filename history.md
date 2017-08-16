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
```

### Setting up Continuous Integration and coverage

```
pip install coveralls

pip freeze > requirements.txt

git add .gitignore .travis.yml requirements.txt
```

### Deploying to Heroku

```
heroku login

write Procfile

foreman start

push static file to master

change wsgi.py
```

### Deployment

```
heroku login

heroku apps:create blog-jeffqian

git push heroku master

heroku config:set DISABLE_COLLECTSTATIC=1

heroku run python3 manage.py makemigrations

heroku run python3 manage.py migrate

heroku open

heroku run python3 manage.py createsuperuser

heroku domains:add www.jifeiqian.com

heroku domains

host www.jifeiqian.com
```

### Syntax highlighting

```
pip install markdown2 Pygments

pip freeze > requirements.txt

mkdir blogengine/static/css

touch blogengine/static/css/main.css

pygmentize -S default -f html > blogengine/static/css/code.css

pygmentize -L styles

pygmentize -S tango -f html > blogengine/static/css/code.css

pygmentize -S monokai -f html > blogengine/static/css/code.css

pip install pygments-style-solarized

pygmentize -S solarizedlight -f html > blogengine/static/css/code.css

pygmentize -S solarizeddark -f html > blogengine/static/css/code.css

pip freeze > requirements.txt
```

### Memcached

```
pip install pylibmc django-pylibmc

pip freeze > requirements.txt

heroku addons:add memcachier:dev
```

### Using Fabric for deployment

```
pip install Fabric

pip3 install Fabric3

pip freeze > requirements.txt

fab deploy
```

### Debugging Django

```
pip install ipdb

pip install django-debug-toolbar

pip freeze > requirements.txt
```

### Optimising static files

```
sudo npm installl -g grunt-cli

npm init

npm install grunt grunt-contrib-cssmin grunt-contrib-concat grunt-contrib-uglify --save-dev
```
