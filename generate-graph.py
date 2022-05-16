#!/usr/bin/env python3

import shutil, os
from owlready2 import *
from rdflib import Graph # doit être chargé après owlready2

# configuration des chemins
dataRootDir     = "../qdmtl-data/"  # répertoire des données (racine), relatif au script
TBox            = "qdmtl-TBox.ttl"  # nom de fichier de la TBox
ABoxDir         = "TTL/"            # répertoire de la ABox
inferenceDir    = "TTL/inference/"  # répertoire des fichiers pour inférence
tmpFile         = "tmp.ttl"         # fichier temporaire (TMP)
inferenceTmpXML = "inf-tmp.rdf.xml" # nom de fichier inférence (TMP)
ntGraphTmp      = "nt-graph-tmp.nt" #
graph           = "qdmtl-graph.ttl" # nom de fichier du graphe (output)

# construction des chemins
TBox = dataRootDir + TBox
ABoxDir = dataRootDir + ABoxDir
graph = dataRootDir + graph
inferenceDir = dataRootDir + inferenceDir
tmpFile = dataRootDir + tmpFile
inferenceTmpXML = dataRootDir + inferenceTmpXML
ntGraphTmp = dataRootDir + ntGraphTmp

# liste des graphes pour Pellet (inférence)
inputReasoner = [file for file in os.listdir(inferenceDir)]

# concat pour inference
# print("concat pour inference")
with open(tmpFile,'w') as tmpf: # tmp file

    with open(TBox,'r') as input:
        shutil.copyfileobj(input, tmpf)

    for file in inputReasoner:
        with open(inferenceDir + file,'r') as input:
            shutil.copyfileobj(input, tmpf)

# conversion
tmpg = Graph()
tmpg.parse(tmpFile) # turtle
tmpg.serialize(destination = inferenceTmpXML, format = "xml") # xml

# inférence
onto_path.append(dataRootDir)
qdmtl = get_ontology("file://" + inferenceTmpXML).load()
with qdmtl:
#    sync_reasoner_pellet()
    sync_reasoner() # Hermit par défaut; Pellet a des problèmes avec anonymous individuals

qdmtl.save(file = ntGraphTmp, format = "ntriples")
print("\n" + "onto_path: " + str(onto_path) + "\n")

# récupérer préfixes
with open(TBox,'r') as f:
    prefixes = re.findall("(@prefix.+)((?:\n.+)+)(\.\n\n)", f.read(3000)) # 3000 char lus
prefixes = "".join([i for i in prefixes[0]])
print(prefixes)

# concat le reste des données
# écrase ficher tmp et le réutilise
with open(tmpFile,'w') as tmpgf:
    tmpgf.write(prefixes)

    for file in os.listdir(ABoxDir):
        if os.path.isdir(ABoxDir + file):
            continue
        with open(ABoxDir + file,'r') as input: # ABox file
            shutil.copyfileobj(input, tmpgf)

# générer le graphe final
qdmtlGraph = Graph()
qdmtlGraph.parse(tmpFile) # turtle
qdmtlGraph.parse(ntGraphTmp) # nt

print("Saving qdmtl-graph")
print("Please wait")
qdmtlGraph.serialize(
    destination = graph,
    base = re.search("@base <(.+)>", prefixes).group(1) + "/",
    format = "ttl"
)
print("Done")

# todo: nettoyage du répertoire
# makefile