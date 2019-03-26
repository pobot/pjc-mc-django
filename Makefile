HOST=eric-laptop.local
REMOTE_DIR=/home/eric/pjc-mc

deploy:
	rsync -Carv \
		--exclude '.*' \
        --exclude fabfile.py \
        --exclude '*.pyc' \
        --exclude __pycache__ \
        --exclude '*.sqlite3' \
        --exclude '*.tgz' \
        --exclude data \
        --exclude requirements-dev.txt \
        --exclude collected_static \
        --exclude teams.txt \
        --exclude tests \
        --exclude pytest.ini \
        ./ $(HOST):$(REMOTE_DIR)/

deploy_db:
	rsync -Carv db.sqlite3 $(HOST):$(REMOTE_DIR)/

run:
	PYTHONPATH=. gunicorn --config gunicorn.conf pjc_mc.wsgi

.PHONY: deploy deploy_db run
