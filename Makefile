include .env
export 

HOST=eric-laptop.local
REMOTE_DIR=/home/eric/pjc-mc
IMAGE=local/pjc_mc
DOCS_LIST := '*'

image:
	docker build -f docker/Dockerfile -t $(IMAGE):latest .

save-image:
	docker save $(IMAGE):latest --output pjc_mc-latest.tar

run-image:
	docker run -it --rm $(IMAGE):latest ./manage.py runserver

dc-up:
	(cd docker && docker-compose up -d)

dc-down:
	(cd docker && docker-compose down)

dc-restart:
	(cd docker && docker-compose restart)

dc-logs:
	(cd docker && docker-compose logs -f django-app)

dc-shell:
	(cd docker && docker-compose exec django-app bash)

docs:
	(cd docker && docker-compose exec django-app ./manage.py make_docs -g $(DOCS_LIST) -o /var/lib/shared/)

run:
	PYTHONPATH=. gunicorn --config gunicorn/config.py pjc_mc.wsgi

runserver:
	./manage.py runserver 0:8000

migrations:
	DATABASE_URL=sqlite:///db.sqlite3 ./manage.py makemigrations

migrate:
	DATABASE_URL=sqlite:///db.sqlite3 ./manage.py migrate

collectstatic:
	./manage.py collectstatic

db-dump:
	(cd docker \
		&& docker-compose exec django-app ./manage.py dumpdata \
			--exclude auth \
			--exclude contenttypes \
			--exclude sessions \
			--exclude admin \
			--output dumpdata.json \
	) \
	&& docker cp django-app:/app/dumpdata.json .

.PHONY: deploy deploy_db run runserver migrations migrate collectstatic docs
