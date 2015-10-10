.PHONY: help clean

help:
	@echo "update - check for new content"
	@echo "recoil - build the Javascript/CSS for recoil"
	@echo "clean - remove all built content"
	@echo "distclean - remove all built and downloaded content"

update: $(wildcard entries/*) $(wildcard pages/*)
	@echo 'TODO: DTRT'

recoil: $(wildcard recoil/*)
	cd recoil
	npm install
	gulp

clean:
	rm -rf index.html
	@echo 'TODO: delete other stuff'

distclean: clean
	@echo 'TODO: delete even more other stuff'
