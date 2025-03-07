*** Basic Django commands ***
python manage.py runserver
python manage.py migrate
python manage.py startapp myapp


*** Create EXE File using the commands below ***

pyinstaller manage_webview.py --name ISMS --icon=assets/logo.ico --hidden-import=django --hidden-import=unicodedata --noconfirm --noconsole --add-data "adminapp/templates:adminapp/templates" --add-data "static:static" --add-data ".env;."



*** If you have the spec file generated, use the command below instead of the ones above ***
pyinstaller ISMS.spec --noconfirm --noconsole







