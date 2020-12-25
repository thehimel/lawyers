
git add . && git commit -m "Message" && git push origin main

python manage.py makemigrations && python manage.py migrate && python manage.py runserver