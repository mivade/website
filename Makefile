CC = ~/src/md2web/md2web.py --template template.html_

all: $(shell find . -name "*.md" | sed 's/md/html/')

%.html: %.md
	$(CC) $<

publish:
	git push
	git push ssh://depalati@depalatis.net/~depalati/git/mike/ master

clean:
	rm *.html
	rm notes/*.html
