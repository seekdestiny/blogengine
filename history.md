### Project Setup

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

### Start App

