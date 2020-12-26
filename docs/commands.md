
conda create --name law python=3.7
conda env remove --namw law
conda create --name law2 --clone law


git add . && git commit -m "Message" && git push origin main

python manage.py makemigrations && python manage.py migrate && python manage.py runserver

pip freeze > requirements.txt