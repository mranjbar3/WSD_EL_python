# -- import hazm library methods
from hazm import Normalizer, WordTokenizer, Lemmatizer, POSTagger


# -- tag any word in sentences as verb or adverb or noun or ...
def pos_tag(i, gateway):
    # print("----------")
    # tagger = POSTagger()
    # input = ["من","آرام","به", "مدرسه","ی","زیبا","رفته بودم", "."]
    # input = ["شیر","سلطان","جنگل", "سرسبز","است"]
    input_var = tokenizer(i)
    # i.split(" ");
    # print("----------")
    # actual = tagger.batchTag(input_var)

    # -- create a java array in python for calling gateway postagger function
    # -- element type of this array is String and its length equal to input_var length
    in_var = gateway.new_array(gateway.jvm.java.lang.String, len(input_var))
    # -- add each input_var element to java String array
    for i in range(0, len(input_var)):
        in_var[i] = input_var[i]
    # -- send array to java listener and wait for response
    # -- the response is type of words in sentence as N,AJ,...
    actual = gateway.entry_point.getPosTagger(in_var)
    pos = []
    # print("---------------------------------------------------------")
    # -- bellow loop replace N with Noun, AJ with Adjective , etc.
    for x in actual:
        pos.append(x.tag().replace("N", "Noun").replace("AJ", "Adjective").replace("V", "Verb").replace("Noune", "Noun")
                   .replace("ADVerb", "Adverb").replace("PUNounC", "PUNC"))

    """
    .replace("PRO","Noun")
    pos.add("Noun");
    pos.add("Noun");
    // pos.add("Verb");
    pos.add("Noun");
    //pos.add("Noun");
    pos.add("Adjective");
    pos.add("Verb");"""
    # -- return words with type
    return pos


def tokenizer(input_var):
    tokenized = []
    normalizer1 = Normalizer(True, False, False)
    normalizer2 = Normalizer(False, True, False)
    normalizer3 = Normalizer(False, False, True)
    word_tokenizer = WordTokenizer(False)
    input_var = normalizer1.normalize(normalizer2.normalize(normalizer3.normalize(input_var)))
    actual = word_tokenizer.tokenize(input_var)
    lemmatizer = Lemmatizer()

    # stemmer = Stemmer

    for x in actual:
        # print(x);
        s = lemmatizer.lemmatize(x)
        if "#" in s and s.split("#")[0] != "":
            tokenized.append(s.split("#")[0] + "ن")
        else:
            tokenized.append(s.replace("#", ""))
    return tokenized


def simple_tokenizer(input_var):
    tokenized = []
    sp = input_var.split(" ")
    # print("Tokenizing.....")
    for i in sp:
        # print(i);
        tokenized.append(i)
    return tokenized


# -- return input!!!
def normalizer(input_var):
    return input_var
