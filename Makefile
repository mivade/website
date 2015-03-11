html:
	cd pelican; pelican content

serve:
	python -m http.server 8000

clean:
	rm -f *.html
	rm -rf author
	rm -rf category
	rm -rf drafts
	rm -rf feeds
	rm -rf tag
	rm -rf theme
