*** Create EXE File using the commands below ***

pyinstaller manage.py --name ISMSAdmin --hidden-import=django --hidden-import=unicodedata"# uniport-isms-admin" --noconfirm

pyinstaller manage.py --name ISMSAdmin --icon=assets/logo.ico --hidden-import=django --hidden-import=unicodedata --noconfirm


pyinstaller manage.py --name ISMSAdmin --icon=assets/logo.ico --hidden-import=django --hidden-import=unicodedata --noconfirm --noconsole

*** If you have the spec file generated, use the command below instead of the ones above ***
pyinstaller ISMSAdmin.spec --noconfirm


