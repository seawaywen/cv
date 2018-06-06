DJANGO_SETTINGS_MODULE ?= django_project.settings
ENV = $(CURDIR)/env
LOCAL_SETTINGS_DIR ?= ../local_config
LOCAL_SETTINGS_PATH = $(LOCAL_SETTINGS_DIR)/settings.py
FLAKE8 = $(ENV)/bin/flake8
GUNICORN = $(ENV)/bin/talisker
PYTHON = $(ENV)/bin/python
PIP = $(PYTHON) $(ENV)/bin/pip
SRC_DIR = $(CURDIR)/src
TEMPLATE_DIR = $(CURDIR)/static/templates
STATIC_SRC_DIR = $(CURDIR)/static_src
LIB_DIR = $(CURDIR)/lib
PYTHONPATH := $(SRC_DIR):$(LIB_DIR):$(CURDIR):$(PYTHONPATH)
DJANGO_MANAGE = $(PYTHON) $(CURDIR)/django_project/manage.py
PROJECT_NAME = memodir

export PYTHONPATH
export DJANGO_SETTINGS_MODULE

$(ENV):
	@virtualenv -p python3 --clear --system-site-packages $(ENV)

install-wheels: ARGS=-r requirements.txt
install-wheels: $(ENV)
	$(PIP) install $(ARGS)

install-wheels-dev: $(ENV) install-wheels 
	$(MAKE) install-wheels ARGS="-r requirements-devel.txt --pre"

collectstatic.deps.mk collectstatic:
# The ouput is verbose but displayed only on errors.  The log file (from a
# working branch) can be used as a reference to diagnose the issues. Comment
# out the redirection to debug.
	@echo "Collecting assets..."
	rm -rf staticfiles
	DJANGO_SETTINGS_MODULE=django_project.settings_build $(DJANGO_MANAGE) collectstatic --noinput --link \
		> logs/collectstatic.log 2>&1 || (cat logs/collectstatic.log && false)

# Asset collection depends on any file or folder in one of the asset
# directories and on the dependency generation command itself.  Asset
# collection also acts as a link checker by resolving all css url(...)
# statements.
collectstatic.deps.mk: src/tools/linkstatic.py

ifneq ($(MAKECMDGOALS), clean)
# Don't fail if the dependency file doesn't exist, running the collection
# will create it.
-include collectstatic.deps.mk
endif


### assets ###

### local config ###
$(LOCAL_SETTINGS_PATH):
	mkdir -p $(LOCAL_SETTINGS_DIR)
	cp django_project/settings.py.example $(LOCAL_SETTINGS_PATH)

bootstrap: $(ENV) $(LOCAL_SETTINGS_PATH) install-wheels-dev

manage:
	$(DJANGO_MANAGE) $(ARGS)

run: ARGS=0.0.0.0:8000
run: collectstatic.deps.mk
	DEVEL=1 $(GUNICORN) --reload --bind=$(ARGS) --workers=2 django_project.wsgi:application


clean-static-assets: 
	rm -fr static_src/node_modules/* 
	rm -f static-assets.deps.mk npm-deps-installed

clean: clean-static-assets
	rm -rf $(ENV)
	rm -rf $(WHEELS_DIR)
	find . -name '*.pyc' | xargs rm -rf
	find . -name '*.~*'  | xargs rm -rf
	rm -f collectstatic.deps.mk
# The files created by compilemessages
	rm -rf src/*/locale


makemessages:
	@echo "Gathering translations for django's apps."
	@for app in `ls $(SRC_DIR) | egrep -v '(test|tools)'`; do \
		mkdir -p "$(SRC_DIR)/$$app/locale"; \
		cd "$(SRC_DIR)/$$app"; \
		$(DJANGO_MANAGE) makemessages -l en -l zh_Hans || exit; \
		cd -; \
	done
	@for app in `ls $(TEMPLATE_DIR)`; do \
		cd "$(TEMPLATE_DIR)/$$app"; \
		$(DJANGO_MANAGE) makemessages -l en -l zh_Hans || exit; \
		cd -; \
	done


compilemessages:
	@echo "Compiling translations for django apps."
	@for app in `ls $(SRC_DIR) | egrep -v '(test|tools)'`; do \
        cd "$(SRC_DIR)/$$app"; \
        $(DJANGO_MANAGE) compilemessages --verbosity 3; \
		cd -; \
    done

lint:
	@$(FLAKE8) --exclude='migrations' --filename='*.py' src/


PG_NAME = $(shell DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'])")
PG_HOST = $(shell DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from django.conf import settings; print(settings.DATABASES['default']['HOST'])")
PG_USER= $(shell DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from django.conf import settings; print(settings.DATABASES['default']['USER'])")
PG_DB_NAME = memodir_pg
PG_DATA_DIR = $(HOME)/docker_pg_data
PG_VAR_RUN_DIR = $(HOME)/docker_pg_var_run
PG_SOCKET = $(PG_VAR_RUN_DIR)/.s.PGSQL.5432

$(PG_DATA_DIR):
	# If the socket didn't exist, db server should be stopped.
	rm -rf $(PG_DATA_DIR)
	mkdir -p $(PG_DATA_DIR) $(PG_VAR_RUN_DIR)
	docker run -d --name $(PG_DB_NAME) -p 5432:5432 -v $(PG_DATA_DIR):/var/lib/postgresql/data -v $(PG_VAR_RUN_DIR):/var/run/postgresql postgres
	@echo 'starting docker...(waiting for 15 secs)'
	sleep 15
	createdb --host=$(PG_HOST) --username=$(PG_USER) $(PG_NAME)
	$(DJANGO_MANAGE) migrate

drop-db:
	@echo 'drop db ...'
	dropdb --host=$(PG_HOST) --username=$(PG_USER) $(PG_NAME)

createsuperuser:
	$(DJANGO_MANAGE) createsuperuser --email=kelvin@memodir.com --username=kelvin

setup-db: $(PG_DATA_DIR)

start-db:
	@echo 'starting db...(waiting for 10 secs)'
	docker start $(PG_DB_NAME)
	sleep 10
	$(DJANGO_MANAGE) migrate

stop-db: $(PG_SOCKET)
	@echo 'stop db...'
	docker stop $(PG_DB_NAME)

destroy-db: stop-db
	@echo 'destroy db...'
	docker rm $(PG_DB_NAME)
	sudo rm -rf $(PG_DATA_DIR) $(PG_VAR_RUN_DIR)


.PHONY: collectstatic makemessages compilemessages setup-db
