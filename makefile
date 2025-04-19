SUBDIRS = $(wildcard */)

.PHONY: all clean $(SUBDIRS)

all: $(SUBDIRS)
	@echo "Build complete for all subdirectories."

clean: $(SUBDIRS)
	@echo "Clean complete for all subdirectories."

$(SUBDIRS):
	@$(MAKE) -C $@ $(MAKECMDGOALS)