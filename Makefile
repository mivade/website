CC = ~/src/md2web/md2web.py --template template.html_
CFLAGS = 
MDFILES = $(shell find . -name "*.md" | sed 's/md/html/')

all: $(MDFILES) template.html_

local: CFLAGS = --base-url '/home/mvd/src/www'
local: $(MDFILES) template.html_

%.html: %.md
	$(CC) $(CFLAGS) $<

publish:
	git push
	git push ssh://depalati@depalatis.net/~depalati/git/mike/ master

clean:
	rm *.html
	rm notes/*.html
