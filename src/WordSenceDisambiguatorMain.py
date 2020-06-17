import sys
from py4j.java_gateway import JavaGateway  # -- py4j a library that run java function from python
import Preprocessor as preprocessor  # -- call Preprocessor file and its methods
import Disambiguator as da  # -- call Disambliguator file and its methods as da
import FarsNetApi as fnet

def main1(input_string):
    # -- create a gateway between farsnet and the python file
    gateway = JavaGateway()
    # -- call farsnet full access
    # fnet = gateway.entry_point.getFnet()
    # input_string = "شیر سلطان جنگل سرسبز است"
    # input_string = "من غذا خوردن سیر شدن"

    # preprocessing the input text
    input_string = preprocessor.normalizer(input_string)
    tokens = preprocessor.tokenizer(input_string)
    input_pos = preprocessor.pos_tag(input_string, gateway)
    gateway.close()

    # -- introduce some variable for storing sentences words and type and etc.
    glosses = []
    elements = []
    scores = []
    max_score_index = []
    examples = []
    pos = []
    sem_cat = []
    ids = []
    synsets = []
    for i in range(0, len(tokens)):
        print("Word:" + tokens[i] + "_POS:" + input_pos[i])
        synsets.append(fnet.getSynsets(tokens[i]))
        ids.append(fnet.getSynsetIds(synsets[i]))
        glosses.append(fnet.getGlosses(synsets[i]))
        examples.append(fnet.getExamples(synsets[i]))
        pos.append(fnet.getPOS(synsets[i]))
        sem_cat.append(fnet.getSemCategory(synsets[i]))

    da.check_pos(synsets, input_pos, pos, ids, glosses, sem_cat, examples)
    for i in range(0, len(tokens)):
        score = []
        maxim = 0
        max_score_index.append(0)
        for j in range(0, len(synsets[i])):
            # fnet.printSynsetElement(synsets[i][j])
            elements.append(fnet.getSynsetElement(synsets[i][j]))
            score1 = da.score_based_on_synsets(elements[len(elements) - 1], input_string)
            score2 = da.cosine_simm(tokens, examples[i][j], glosses[i][j])
            score3 = da.score_based_on_synsets(fnet.getSynsetsRelations(synsets[i][j]), input_string)
            # print(score1+score2+score3+":"+j)
            score.append(score1 + score2 + score3)
            if maxim < score1 + score2 + score3:
                max_score_index.pop()
                max_score_index.append(j)
                maxim = score1 + score2 + score3
                # print(j)
            print("Id:", str(ids[i][j]), "_", str(pos[i][j]), "_", str(sem_cat[i][j]), "_gloss:",
                  str(glosses[i][j]))
            print("Score:", str(score1), "_", str(score2), "_", str(score3))
            print("Examples:", str(examples[i][j]))
        scores.append(score)

    out = "{"
    for i in range(0, len(tokens)):
        index = max_score_index[i]
        if len(glosses[i]) != 0 and len(scores[i]) != 0:
            out += '"' + tokens[i] + '"' + ":" + '"' + glosses[i][index] + '"'
            print("Word:", tokens[i], "_Score:", str(scores[i][index]),
                  "_selected gloss:", str(glosses[i][index]))
        else:
            out += '"' + tokens[i] + '"' + ":" + "یافت نشد" + '"'
            print("Word:", tokens[i], "_Score:None_selected gloss:None")
        out += ","
    out += "}"
    return out.replace(",}", "}")


def main2(input_string):
    gateway = JavaGateway()
    fnet = gateway.entry_point.getFnet()
    # inputString = "شیر سلطان جنگل سرسبز است"
    # inputString = "من غذا خوردن سیر شدن"

    # preprocessing the input text
    input_string = preprocessor.normalizer(input_string)
    tokens = preprocessor.tokenizer(input_string)
    input_pos = preprocessor.pos_tag(input_string, gateway)

    glosses = []
    elements = []
    scores = []
    max_score_index = []
    examples = []
    pos = []
    sem_cat = []
    ids = []
    synsets = []
    for i in range(0, len(tokens)):
        # print("Word:"+tokens.get(i)+"_POS:"+input_pos.get(i))
        synsets.append(fnet.getSynsets(tokens[i]))
        ids.append(fnet.getSynsetIds(synsets[i]))
        glosses.append(fnet.getGlosses(synsets[i]))
        examples.append(fnet.getExamples(synsets[i]))
        pos.append(fnet.getPOS(synsets[i]))
        sem_cat.append(fnet.getSemCategory(synsets[i]))

    da.check_pos(synsets, input_pos, pos, ids, glosses, sem_cat, examples)
    for i in range(0, len(tokens)):
        score = []
        max = sys.maxsize
        max_score_index.append(0)
        for j in range(0, len(synsets[i])):
            # fnet.printSynsetElement(synsets.get(i)[j])
            elements.append(fnet.getSynsetElement(synsets[i][j]))
            score1 = da.score_based_on_synsets(elements[len(elements) - 1], input_string)
            score2 = da.cosine_simm(tokens, examples[i][j], glosses[i][j])
            score3 = da.score_based_on_synsets(fnet.getSynsetsRelations(synsets[i][j]), input_string)
            # print(score1+score2+score3+":"+j)
            score.append(score1 + score2 + score3)
            if max < score1 + score2 + score3:
                max_score_index.remove(len(max_score_index) - 1)
                max_score_index.append(j)
                max = score1 + score2 + score3
                # print(j)
            # print("Id:" + ids[i][j] + "_" + pos[i][j] + "_" + sem_cat[i][j] + "_gloss:" + glosses[i][j])
            # print("Score:"+score1+"_"+score2+"_"+score3)
            # print("Examples:"+examples[i])[j])
        scores.append(score)

    out = ""
    for i in range(0, len(tokens)):
        index = max_score_index[i]
        if len(glosses[i]) != 0 and len(scores[i]) != 0:
            out = out + str(ids[i][index]) + ","  # '"'+ tokens.get(i) +'"'+":" +'"'+ glosses[i].get(index)+'"'
            # print("Word:" + tokens.get(i)+ids[i].get(index) +"_Score:" + scores[i].get(index)+"_selected gloss:" + glosses[i].get(index))
        else:
            out += "0,"  # '"'+ tokens.get(i) +'"'+ ":"+"یافت نشد"+'"'
            # print("Word:" + tokens.get(i) + "_Score:None_selected gloss:None")
        # out += ","
    out += "}"
    # print("out:" + out)
    # out = out.replace(",}", "}")
    return out


# -- add your sentence in this variable
sentence = "شیر سلطان جنگل سرسبز است. من جنگل را دوست داشتن."
# sentence = "شیر سلطان جنگل سرسبز است."
sentence = "خدا"
main1(sentence)
