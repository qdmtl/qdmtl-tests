# Cas de test — QDMTL

Ce dépôt contient les scénarios liés aux cas de test du [projet QDMTL](https://qdmtl.ca). Il s’agit principalement de notes de travail.

Plus d’informations sur le projet QDMTL :

- [https://qdmtl.ca](https://qdmtl.ca)

La méthodologie de développement du jeu de données est basée sur :

- Peroni, S. (2016). A Simplified Agile Methodology for Ontology Development. In Proceedings of the 13th OWL: Experiences and Directions Workshop and 5th OWL reasoner evaluation workshop (OWLED-ORE 2016). https://w3id.org/people/essepuntato/papers/samod-owled2016.html

## Test Case Definition

Source : Peroni (2016), [https://essepuntato.it/samod/](https://essepuntato.it/samod/)

| Abéviation | Définition |
|---:|---|
| MS  | motivating scenario |
| CQ  | scenario-related informal competency questions |
| GoT  | glossary of terms |
| TBox  | formal model implementing the description introduced in the motivating scenario |
| ABox  | exemplar dataset implementing all the examples described in the motivating scenario according to the TBox |
| SQ  | set of queries formalising the informal competency questions |

## Cas de test

- [x] 001-les numéros d’inventaire du plan d’expropriation
- [ ] 002-le contexte archivistique plus large de la pièce d’archives
- [x] 003-les objets représentés par les photographies d’archives (bâtiments disparus)
- [x] 004-le type de contenu et les instanciations des pièces d’archives
- [ ] 005-les territoires

### À venir

- [ ] les occupants des immeubles (groupes et organisations), avec fenêtre temporelle
  - [ ] les adresses civiques des organisations
- [ ] les témoignages
<!-- - [ ] inventory number status (certain, uncertain, unreadable, etc.) -->

## Protocoles

> :warning: **Cette procédure est obsolète. Voir section `Test` ci-dessous.**

Lorsque le *modelet* est considéré comme prêt à tester et que l’échantillon de données est prêt :

1. commit sur `qdmtl-onto` `dev`, puis `$ git checkout tc-<id>`;
2. générer l’échantillon de données RDF (an ABox as *exemplar dataset*) lié au cas de test
3. concaténer l’ABox généré à la TBox (*modelet*) sur la branche `tc-<id>`;
4. parser et indenter avec OWL API : écraser l’output de la concaténation;
5. tester;
6. important : lorsque le test est concluant, commit sur la branche `tc-<tcID>`;
7. si nécessaire, `cherrypick` vers branche `dev`, si des commits pertinents ont eu lieu..

### Test

1. commit sur `qdmtl-onto` `dev`, puis `$ git checkout tc-<id>`;
2. `$ make` sur `qdmtl-test-cases`
3. tester;
4. important : lorsque le test est concluant, commit sur la branche `tc-<tcID>`;
5. si nécessaire, `cherrypick` vers branche `dev`, si des commits pertinents ont eu lieu..

### Merge Models et déploiement

Lorsqu’un cas de test a été effectué avec succès :

1. procéder à l’identification du *modelet* sur la branche `dev` : `$ git tag m-<tcID>` (lightweight tag) : par exemple `$ git tag m-001`;
  - Dans le contexte du projet QDMTL, le *modelet* peut inclure des entités de modèles externes;
  - La version du *modelet* ne relève *pas* du versionnage sémantique; il s’agit d’un système d’identification interne.
2. fusionner le modèle actuel avec le *modelet* : toujours sur la branche `dev` : `$ git merge main` (s’il n’y a pas de modification sur `main`, le modèle `dev` est le plus récent, donc output == `already up to date`);
3. si nécessaire : tester le nouveau modèle;
4. refactoriser;
5. si nécessaire, versionner le modèle : `$ git tag -a v<version> -m "<label du tag>"`;
6. générer sérialisation RDF/XML de la TBox
7. `$ git checkout main` puis `$ git merge dev` (`--no-ff`?).
8. `$ make`
9. `$ ./push.sh`

Ne pas oublier de pousser les tags.

### Generate Complete Graph

> :warning: **Cette procédure est obsolète. Elle est remplacée par le `makefile`.**

Générer le graphe et charger dans l’entrepôt :

1. Copier la dernière version du modèle (disponible dans `qdmtl-ontology`) dans `qdmtl-data` : `/qdmtl/qdmtl-data/qdmtl-TBox.ttl`
2. Générer les plus récentes ABox à partir des fichiers CSV : `$ python3 batch-convert-csv-ttl.py`
3. ~~Placer les données à soumettre au moteur d’inférence dans le répertoire prévu à cet effet~~ voir `generate-graph.py` config.
4. Générer le graphe : `$ python3 generate-graph.py`
5. SPARQL LOAD : `$ php load-data-local.php`

## NOTES

Si c’est commun à record et instantiation, ça va dans ContentType.

- **ContentType**
  - categorizes a Record Resource;
  - communication;
- **CarrierType**
  - categorizes an Instantiation;
  - physical material in or on which information is represented;
  - is independent of its content
- **RepresentationType**
  - categorizes an Instantiation
  - method of recording
  - bit rate for audi
  - resolution for digital images
  - encoding format for video etc.
  - sketch (Representation Type: graphic)
  - GIS-coded elements (Representation Type: computer).

Types de représentation, qui est plus du type de contenu selon rico... :

- visuelle
- textuelle
- sonore (audio).