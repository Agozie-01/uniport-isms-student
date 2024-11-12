*** Basic Django commands ***
python manage.py runserver
python manage.py migrate
python manage.py startapp myapp


*** Create EXE File using the commands below ***

pyinstaller manage_webview.py --name ISMSAdmin --icon=assets/logo.ico --hidden-import=django --hidden-import=unicodedata --noconfirm --noconsole --add-data "adminapp/templates:adminapp/templates" --add-data "static:static" --add-data ".env;."



*** If you have the spec file generated, use the command below instead of the ones above ***
pyinstaller ISMSAdmin.spec --noconfirm --noconsole

# .env file
DB_ENGINE=django.db.backends.mysql
DB_NAME=isms_db_prod
DB_USER=admin_isms
DB_PASSWORD="@193isMS"
DB_HOST=mysql.bittopay.ng
DB_PORT=3306


