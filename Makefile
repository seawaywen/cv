DJANGO_SETTINGS_MODULE ?= django_project.settings
ENV = $(CURDIR)/env
LOCAL_SETTINGS_DIR ?= ../local_config
LOCAL_SETTINGS_PATH = $(LOCAL_SETTINGS_DIR)/settings.py
FLAKE8 = $(ENV)/bin/flake8
GUNICORN = $(ENV)/bin/talisker
PYTHON = $(ENV)/bin/python
PIP = $(PYTHON) $(ENV)/bin/pip
SRC_DIR = $(CURDIR)/src
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
	#$(PIP) install --find-links=$(WHEELS_DIR) --no-index $(ARGS)
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

ifneq ($(MAKECMDGOALS),clean)
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
