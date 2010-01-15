# A simple Makefile to generate the documentation

DOCSBUILD=../build/docs/site
FLEXIREST=../bin/flexirest

all: docsdir statics generate

docsdir:
	mkdir -p $(DOCSBUILD)

statics: flexirest.css
	cp flexirest.css $(DOCSBUILD)/

generate: docsdir statics *.txt
	$(FLEXIREST) < index.txt > $(DOCSBUILD)/index.html --template=template.html
	$(FLEXIREST) < quick-manual.txt > $(DOCSBUILD)/quick-manual.html --template=template.html
	$(FLEXIREST) < download.txt > $(DOCSBUILD)/download.html --template=template.html
	$(FLEXIREST) < dependencies-0.8.4-dev.txt > $(DOCSBUILD)/deps-0.8.4dev.html --template=template.html
	$(FLEXIREST) < requirements.txt > $(DOCSBUILD)/requirements.html --template=template.html

deploy: generate
	rsync -rv $(DOCSBUILD)/* flexisite:public_html/flexirest

.PHONY: all
