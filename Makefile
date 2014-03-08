CC = ./md2web.py --template template.html_

all: $(shell find . -name "*.md" | sed 's/md/html/')

%.html: %.md
	$(CC) $<

clean:
	rm *.html
