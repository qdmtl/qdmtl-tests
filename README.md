# Cas de test - QDMTL

## Test Case Definition

- MS : motivating scenario;
- CQ : scenario-related informal competency questions;
- GoT : glossary of terms;
- TBox : formal model implementing the description introduced in the motivating scenario;
- ABox : exemplar dataset implementing all the examples described in the motivating scenario according to the TBox;
- SQ : set of queries formalising the informal competency questions.

Source : [https://essepuntato.it/samod/](https://essepuntato.it/samod/)

## Cas de test

- [x] 001-les numéros d’inventaire du plan d’expropriation
- [ ] 002-le contexte archivistique plus large de la pièce d’archives
- [ ] 003-les objets représentés par les photos d'archives (immeubles et lieux disparus)

### À venir

- [ ] les territoires administratifs au fil des années
- [ ] les voies de communication
- [ ] les instanciations des pièces d'archives (et leur fichiers numériques s'il y a lieu)
- [ ] les organisations occupant les immeubles, avec fenêtre temporelle
- [ ] les adresses civiques
- [ ] les personnes physiques
- [ ] les témoignages

## Protocoles

### Merge Models

Lorsqu'un cas de test a été effectué avec succès :

1. procéder à l'identification du *modelet* dans la branche `dev` : `$ git tag m<version>` (lightweight tag) : par exemple `$ git tag m001`;
  - Dans le contexte du projet QDMTL, le *modelet* peut inclure des entités de modèles externes;
  - La version du *modelet* ne relève *pas* du versionnage sémantique; il s'agit d'un système d'identification interne.
2. fusionner le modèle actuel avec le *modelet* : toujours sur la branche `dev` : `$ git merge main`;
3. tester le nouveau modèle (protocole à détailler);
4. refactoriser;
5. Si nécessaire : `$ git tag -a v<version> -m "<label du tag>"`;
6. `$ git checkout main` puis `$ git merge dev` (`--no-ff`?).

Ne pas oublier de pousser les tags.

TODO : script

### Generate Data

1. Copier la dernière version du modèle (disponible dans qdmtl-ontology) dans qdmtl-data
2. Renommer qdmtl-data.ttl
3. Py : générer les plus récentes ABox à partir des fichiers CSV
4. Py : concaténer les ABox à qdmtl.ttl
5. Exécuter Pellet (TODO : tester les options, éviter les inférences superflues)
6. SPARQL LOAD

TODO : script