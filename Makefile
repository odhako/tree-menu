start:
	poetry run python manage.py runserver

shell:
	poetry run python manage.py shell_plus

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

req:
	poetry export --without-hashes -f requirements.txt -o requirements.txt
