.PHONY: doc
doc:
	a2x --doctype manpage --format manpage README.asciidoc

.PHONY: clean
clean:
	rm -f *.7
	rm -f *.pyc
	rm -f *.pyo
