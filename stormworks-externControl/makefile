
# List of files to compile
LUA_SRC = $(wildcard src/script/*.lua)
HTML_SRC = $(wildcard src/front/*.html)
TS_SRC = $(wildcard src/front/*.ts) $(wildcard src/front/**/*.ts)
SCSS_SRC = $(wildcard src/front/*.scss)
svg_SRC = $(wildcard src/front/icons/*.svg)
tff_SRC = $(wildcard src/front/fonts/*.ttf)
PY_SRC = $(wildcard src/stormworks_server/*.py) $(wildcard src/stormworks_server/**/*.py) 

SRC = $(LUA_SRC) $(HTML_SRC) $(svg_SRC) $(tff_SRC) src/pyproject.toml

LUA_CONF =
HTML_CONF =
TS_CONF = package.json
SCSS_CONF =
PY_CONF = src/pyproject.toml


PY_TARGETS = $(patsubst src/stormworks_server/%.py, dist/stormworks_server/%.py, $(PY_SRC))
CSS_TARGETS = $(patsubst src/%.scss, dist/%.css, $(SCSS_SRC))
JS_TARGETS = $(patsubst src/%.ts, dist/%.js, $(TS_SRC))

PY_MODULE = dist/stormworks_server-0.1.0-py3-none-any.whl

TARGETS = $(patsubst src/%, dist/%, $(SRC)) $(CSS_TARGETS) $(JS_TARGETS)



TS_OPTIONS =  	--target es2016 \
				--module es6 \
				--moduleResolution node \
				--declaration \
				--sourceMap \
				--removeComments \
				--forceConsistentCasingInFileNames \
				--strict \
				--noImplicitAny \
				--strictNullChecks \
				--strictFunctionTypes \
				--strictPropertyInitialization \
				--noImplicitThis \
				--alwaysStrict \
				--noUnusedLocals \
				--noUnusedParameters \
				--noImplicitReturns \
				--noFallthroughCasesInSwitch \
				--noUncheckedIndexedAccess \
				--noImplicitOverride \

.PHONY: all clean start install

all: $(TARGETS) $(PY_TARGETS) $(PY_MODULE)

dist/front/style.css: $(SCSS_SRC) $(SCSS_CONF)
	@mkdir -p $(@D)
	sass $< $@

dist/front/%.js: src/front/%.ts $(TS_CONF)
	@mkdir -p $(@D)
	tsc $< $(TS_OPTIONS) --outdir dist/front

dist/script/%.lua: src/script/%.lua $(LUA_CONF)
	@mkdir -p $(@D)
	luamin -f $< > $@


$(PY_MODULE): $(PY_TARGETS) dist/pyproject.toml $(PY_CONF)
	@mkdir -p $(@D)
	env/bin/python3 -m pip install --upgrade setuptools wheel
	cd dist && ../env/bin/python3 -m build --wheel --outdir .


dist/%.py: src/%.py $(PY_CONF)
	@mkdir -p $(@D)
	cp $< $@

dist/%: src/% # if no rule is found, copy the file
	@mkdir -p $(@D)
	cp $< $@

env/bin/stormworks_server: $(PY_MODULE)
	env/bin/python3 -m pip install $(PY_MODULE) --force-reinstall

install: all env/bin/stormworks_server

start: all install
	env/bin/stormworks_server

tests: all install
	clear
	pytest tests/server/ --junit-xml=tests/server/report.xml -vv

clean:
	rm -rf dist