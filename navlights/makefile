
# List of files to compile
SRC = $(wildcard src/*.lua)

TARGETS = $(patsubst src/%.lua, dist/%.lua, $(SRC))

all: $(TARGETS)



dist/%.lua: src/%.lua
	@mkdir -p $(@D)
	luamin -f $< > $@

clean:
	rm -rf dist