start:
	python3 manage.py runserver

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

runserver_plus:
	python3 manage.py runserver_plus --cert-file cert.crt
shell:
	python3 manage.py shell