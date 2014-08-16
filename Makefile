CC = ~/src/md2web/md2web.py --template 'templates/main.html'
CFLAGS = 
MDFILES = $(shell find . -name "*.md" | sed 's/md/html/')

all: $(MDFILES) templates/main.html

local: CFLAGS = --base-url '/home/mvd/src/www'
local: $(MDFILES) templates/main.html

%.html: %.md
	$(CC) $(CFLAGS) $<

publish:
	git push
	git push ssh://depalati@depalatis.net/~depalati/git/mike/ master

clean:
	rm *.html
	rm notes/*.html
