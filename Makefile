local-run:
	# make translate
	docker-compose -f local.yml up

local-build:
	docker-compose -f local.yml build

deploy:
	docker-compose -f production.yml up --build -d

stop:
	docker-compose -f local.yml down

prod-stop:
	docker-compose -f production.yml down

django-manage:
	docker-compose -f local.yml run --rm django python manage.py $(args)

migrate:
	docker-compose -f local.yml run --rm django python manage.py makemigrations
	docker-compose -f local.yml run --rm django python manage.py migrate

prod-migrate:
	docker-compose -f production.yml run --rm django python manage.py makemigrations
	docker-compose -f production.yml run --rm django python manage.py migrate

createsuperuser:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

prod-createsuperuser:
	docker-compose -f production.yml run --rm django python manage.py createsuperuser

translate:
	docker-compose -f local.yml run --rm django django-admin makemessages --all --ignore .venv --ignore docs --ignore pedtrid/templates/account --ignore pedtrid/users
	docker-compose -f local.yml run --rm django django-admin compilemessages --ignore .venv --ignore docs --ignore pedtrid/templates/account --ignore pedtrid/users

test:
	docker-compose -f local.yml run django pytest $(args)

test-coverage:
	docker-compose -f local.yml run django coverage run -m pytest
	docker-compose -f local.yml run django coverage html
	open htmlcov/index.html

local-django-shell:
	docker-compose -f local.yml run --rm django python manage.py shell

prod-django-shell:
	docker-compose -f production.yml run --rm django python manage.py shell

type-check:
	docker-compose -f local.yml run --rm django mypy data_pipeline_manager
