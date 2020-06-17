from Farsnet import SynsetService


def getSynsets(word):
    return SynsetService.getSynsetsByWord("EXACT", word)


def getSynsetIds(synsets):
    ids = []
    for synset in synsets:
        ids.append(synset.id)
    return ids


def getGlosses(synsets):
    glosses = []
    for synset in synsets:
        glosses.append(synset.gloss)
    return glosses


def getExamples(synsets):
    example = []
    for synset in synsets:
        example.append(synset.example)
    return example


def getPOS(synsets):
    pos = []
    for synset in synsets:
        pos.append(synset.pos)
    return pos


def getSemCategory(synsets):
    sem = []
    for synset in synsets:
        sem.append(synset.semanticCategory)
    return sem


def getPOSfromID(fnIds):
    sem = []
    for fnId in fnIds:
        # print(fnIds)
        s = SynsetService.getSynsetById(fnId).getPos()
        sem.append(s)
        # print(s)
    return sem


def printSynsetElement(fnSynset):
    # print("Synset:{")
    for j in range(0, len(fnSynset.getSenses())):
        fnSense = fnSynset.getSenses()[j]
        # print(fnSense.getWord().getValue().elementAt(0) + "_" + fnSense.getId() + " ,")
    # print("}")


def getSynsetElement(fnSynset):
    elements = []
    for j in range(0, len(fnSynset.getSenses())):
        fnSense = fnSynset.getSenses()[j]
        s = fnSense.word.defaultValue.strip()
        elements.append(s)
        # print(s + "_" + fnSense.getId() + " ,")
    return elements


def getSynsetElement_2(synset):
    elements = []
    for syn in synset:
        for sense in syn.getSenses():
            elements.append(sense.value.strip())
    return elements


def getSynsetsRelations(synset):
    relatedWords = []
    synsetRelations = synset.getSynsetRelation()
    for synsetRelation in synsetRelations:
        if synsetRelation.synsetId1 == synset.id:
            for i in getSynsetElement_2(synsetRelation.getSynset2()):
                relatedWords.append(i)
    return relatedWords


def FNAPIUse(word):
    # find all synset containd the word
    fnSynsets = SynsetService.getSynsetsByWord("LIKE", word)
    # print every    synset
    for fnSynset in fnSynsets:
        # print("Synset:{")
        for j in range(0, len(fnSynset.getSenses())):
            fnSense = fnSynset.getSenses()[j]
            # print(fnSense.getWord().getValue().elementAt(0)+"_"+fnSense.getId()+" ,")
        # print("}")
        # print("Father[s]:")
        fathers = fnSynset.getSynsetRelations()
        for synsetRelation in fathers:
            if synsetRelation.getSynset1().getId() == fnSynset.getId() and synsetRelation.getReverseType().equalsIgnoreCase(
                    "Hypernym"):
                # print("Synset:{")
                father = synsetRelation.getSynset2()
                for j in range(0, len(father.getSenses())):
                    fnSense = father.getSenses()[j]
                    # print(fnSense.getWord().getValue().elementAt(0)+"_"+fnSense.getId()+" ,")


# print("}")
# print("********************")
# print(".......................")
# print(fnSynsets.get(i).getGloss())
""" print(".......................")
 f = fnSynsets[i].getSenses()
 for j in range(0,len(f)):
     print(".......")
     w = f[j].getWord().getValue()
     for k in range(0, len(w)):
         print(w[k] + "_" + f[j].getId())
"""
b=[]
b.append(SynsetService.getSynsetGlosses(11940))
b.append(SynsetService.getSynsetGlosses(11940))
print(b)
print(b[0])