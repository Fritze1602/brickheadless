# ✨ Developer-Shortcuts

sync:
	python manage.py sync_collections

migrate:
	python manage.py makemigrations && python manage.py migrate

run:
	python manage.py runserver

admin:
	python manage.py createsuperuser

shell:
	python manage.py shell

reset:
	python manage.py flush