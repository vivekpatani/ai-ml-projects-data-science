from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from collections import Counter
from nltk.corpus import stopwords
from nltk import pos_tag
from collections import defaultdict
import os
from subprocess import call


def readfile(filename, location="input/"):
    """
    Read the input files
    """
    file_data = open(location + filename).read()
    file_data = file_data.split('.')
    return file_data


def print_meanings(word):
    """
    Using NLTK to obtain Syn Set
    """
    synsets = wn.synsets(word)
    print("Different Meanings:")
    for item in range(len(synsets)):
        print(str(item + 1) + ". " + str(synsets[item].definition()))
    print("\n")


def tokenise(text):
    """
    Tokenise the given text using NLTK
    """
    onetext = ""
    # Compress Data as it is a list
    for sentences in text:
        onetext += sentences
    tokens = word_tokenize(onetext.lower())
    return tokens


def frequencyProfiler(tokens):
    """
    Returns Frequency Profile
    """
    return Counter(tokens)


def removeStopWords(tokens):
    """
    Remove Stop words using NLTK
    """
    stopw = stopwords.words("english")
    for each_word in tokens:
        if (each_word in stopw):
            tokens.remove(each_word)
    return tokens


def POSTagger(tokens):
    """
    Tag given Tokens using NLTK
    """
    postags = [ (x[0], x[1][0]) for x in pos_tag(tokens) ]
    tags = list(set(x[1] for x in postags))
    return postags, tags


def fit(posTokens, tags, attrib_class=0):
    """
    Generating POSTokens for TimBL
    """
    leftOfToken = defaultdict(Counter)
    rightOfToken = defaultdict(Counter)

    model = []

    lenPosTokens = len(posTokens)
    for i in range(lenPosTokens):
    	token = posTokens[i]
    	if (i > 0):
    		ltag = posTokens[i - 1][1]
    		leftOfToken[token][ltag] += 1
    	if i < lenPosTokens - 1:
    		rtag = posTokens[i + 1][1]
    		rightOfToken[token][rtag] += 1

    for token in leftOfToken.keys():
    	leftVector = []
    	rightVector = []
    	for tag in tags:
    		leftVector.append(leftOfToken[token][tag])
    		rightVector.append(rightOfToken[token][tag])
    	rightVector.append(attrib_class)
    	model += [leftVector + rightVector]

    return model

def dump_model (model, dir="model/", filename="output.txt"):
    """
    Dumps Model in a given file
    Which can be used for TiMBL
    """
    with open(dir + filename, 'a') as output:
        for vectors in model:
        	for vector in range(len(vectors)):
        		output.write(str(vectors[vector]) + "\t")
        	output.write("\n")
    output.close()
    print("Dumping is over!")

def main():

    # Defining word to disambiguate
    ambiguous = "driver"
    print_meanings(ambiguous)

    # Loading Train Files
    print("Loading Train Text...")
    train1 = readfile("input1.txt")
    train2 = readfile("input2.txt")
    
    # Loading Test Files
    print("Loading Train Text...")
    test1 = readfile("test1.txt")
    test2 = readfile("test2.txt")

    # Tokenise
    print("Tokenising Train Data...")
    # tokens1 = removeStopWords(tokenise(train1))
    # tokens2 = removeStopWords(tokenise(train2))
    tokens1 = tokenise(train1)
    tokens2 = tokenise(train2)

    # Tokenise
    print("Tokenising Test Data...")
    # tokens1 = removeStopWords(tokenise(train1))
    # tokens2 = removeStopWords(tokenise(train2))
    tokenstest1 = tokenise(test1)
    tokenstest2 = tokenise(test2)

    # Generate Frequency Profiles
    print("Generating Frequency Profiles....")
    freqp1 = frequencyProfiler(tokens1)
    freqp2 = frequencyProfiler(tokens2)

    # Tag Tokens
    print("Tagging Trian Tokens...")
    pos1, tags1 = POSTagger(tokens1)
    pos2, tags2 = POSTagger(tokens2)

    # Tag Tokens
    print("Tagging Test Tokens...")
    postest1, tagstest1 = POSTagger(tokenstest1)
    postest2, tagstest2 = POSTagger(tokenstest2)

    # Tags
    print("Fetching Unique Tokens to generate model for TimBL...")
    tags = set(tags1 + tags2 + tagstest1 + tagstest2) 
    
    # Prepare Model
    try:
    	os.remove("model/model-collocation.txt")
    	print("Deleting Preexisting Models")
    	os.remove("model/test-collocation1.txt")
    	os.remove("model/test-collocation1.txt")
    except OSError: pass
    print("Preparing File for TimBL input")
    model1 = fit(pos1, tags)
    model2 = fit(pos2, tags, attrib_class=1)

    modeltest1 = fit(postest1, tags)
    modeltest2 = fit(postest2, tags, attrib_class=1)

    print("Dumping Models to a file for TimBL to read.")
    dump_model(model1, filename="model-collocation.txt")
    dump_model(model2, filename="model-collocation.txt")

    dump_model(modeltest1, filename="model-collocation-test1.txt")
    dump_model(modeltest2, filename="model-collocation-test2.txt")

    # Training using TiMBL
    call(["timbl", "-f", "model/model-collocation.txt", "-t", "model/model-collocation-test1.txt", "-mC", "+v", "cm"])
    call(["timbl", "-f", "model/model-collocation.txt", "-t", "model/model-collocation-test2.txt", "-mC", "+v", "cm"])

if __name__ == "__main__":
    main()