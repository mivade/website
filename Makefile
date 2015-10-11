.PHONY: help clean

help:
	@echo "update - check for new content"
	@echo "recoil - build the Javascript/CSS for recoil"
	@echo "clean - remove all built content"
	@echo "distclean - remove all built and downloaded content"

update: $(wildcard entries/*) $(wildcard pages/*) index.json

index.json:
	node update.js

recoil: $(wildcard recoil/*)
	cd recoil
	npm install
	gulp

clean:
	rm -rf index.html
	rm -rf index.json

distclean: clean
	@echo 'TODO: delete even more other stuff'
