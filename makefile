# Makefile

SHELL := /bin/bash

# Variables
ONTO = ../qdmtl-ontology/qdmtl.ttl
TBOX = ../qdmtl-data/qdmtl-TBox.ttl
GRAPH = ../qdmtl-data/qdmtl-graph.ttl
CONVERT = convert-build.txt

.PHONY: clean

all: $(TBOX) $(GRAPH) $(CONVERT)

$(TBOX): $(ONTO)
	@echo "Copier la TBox..."
	cp $(ONTO) $@

$(CONVERT): ../qdmtl-data/CSV/*
	@echo "Convertir CSV --> TTL"
	./batch-convert-csv-ttl.py
	echo `date +%s` >> $@

$(GRAPH): $(TBOX) $(CONVERT)
	@echo "Générer le graphe"
	source .venv/bin/activate && ./generate-graph.py && deactivate
	@echo "Chargement dans l'entrepôt local..."
	cp $@ ~/public_html/dev-web/qdmtl-triple-store/process/qdmtl-graph.ttl
	cd ~/public_html/dev-web/qdmtl-triple-store/process/ && ./load-data-local.php

clean:
	@echo "foobar"