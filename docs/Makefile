# A simple Makefile to generate the documentation

DOCSBUILD=../build/docs
FLEXIREST=../bin/flexirest

all: docsdir statics generate

docsdir:
	mkdir -p $(DOCSBUILD)

statics: flexirest.css
	cp flexirest.css $(DOCSBUILD)/

generate: docsdir statics introduction.txt quick-manual.txt
	$(FLEXIREST) < introduction.txt > $(DOCSBUILD)/index.html --template=template.html
	$(FLEXIREST) < quick-manual.txt > $(DOCSBUILD)/quick-manual.html --template=template.html

deploy: generate
	scp -r $(DOCSBUILD)/* flexisite:public_html/flexirest

.PHONY: all