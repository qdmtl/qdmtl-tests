import csv, re, os

# Paramètres
inputFolder = '../qdmtl-data/CSV/'
outputFolder = '../qdmtl-data/TTL/'
filesWithBlankNodesAndNumberOfBN = {
    'qdmtl-Record.csv' : 2
}

# liste de fichiers
files = os.listdir(inputFolder)

for file in files:
    if file in filesWithBlankNodesAndNumberOfBN.keys():
        continue
    filesWithBlankNodesAndNumberOfBN[file] = 0

for inputFile, number in filesWithBlankNodesAndNumberOfBN.items():
    inputFilePath = inputFolder + inputFile
    outputFile = re.match("(.+)\.csv", inputFile).group(1)
    outputFile = outputFolder + outputFile + '-ABox.ttl'

    # Initialisations
    extractedData = []
    propWithBlankNodeValue = {}
    propWithBlankNode = []
    numberOfPropWithBlankNode = number

    # Chargement des données
    with open(inputFilePath, 'r+', newline = '') as csvFile:
        extractedData = [
            dict(row) for row in csv.DictReader(csvFile, delimiter = ',')
        ]

    l = len(extractedData[0])

    # Identification des propriétés avec noeuds vides
    for i, key in enumerate(extractedData[0].keys()):
        if i > l - numberOfPropWithBlankNode - 1:
            propWithBlankNode.append(key)

    # Écriture du fichier Turtle
    with open(outputFile, 'w') as ABox:
        for subject in extractedData:
            for i, (property, value) in enumerate(subject.items()):

                if value == '':
                    continue

                # si blank node, les props sont traitées en dehors de la boucle
                if 1 < i < len(subject) - numberOfPropWithBlankNode:
                    assertions += ' ;\n'

                # voir structure switch Python 3.10
                if property == 'URI':
                    assertions = value + ' rdf:type owl:NamedIndividual ,\n'
                elif property == 'rdf:type':
                    assertions += '\t\t' + subject['rdf:type']
                elif property in propWithBlankNode :
                    propWithBlankNodeValue[property] = value
                else:
                    assertions += '\t' + property + ' ' + value

            if propWithBlankNodeValue:

                assertions += ' ;\n\trico:hasOrHadIdentifier '

                for i, (property, value) in enumerate(propWithBlankNodeValue.items()):
                    assertions += '[\n'
                    assertions += '\t\trdf:type rico:Identifier ;\n'
                    assertions += '\t\trico:hasIdentifierType ' + property + ' ;\n'
                    assertions += '\t\trico:textualValue ' + value
                    if property == 'vocab:inventoryNumber':
                      assertions += '\t\trdf:value ' + value + '^^xsd:integer'
                    assertions += '\n\t]'

                    if i < len(propWithBlankNodeValue) - 1:
                        assertions += ' , '

                else:
                    propWithBlankNodeValue = {}

            assertions += ' .\n\n'
            ABox.write(assertions)
