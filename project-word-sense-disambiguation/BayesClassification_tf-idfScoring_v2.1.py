"""Used tf-idf to calculate the scores for each token in our Frequency profile."""

from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from math import log

stopw = stopwords.words('english')


# tokenizer = RegexpTokenizer(r'\w+')

class MyTextCollection(object):
    def __init__(self, data):
        self._texts = data
        # if hasattr(source, 'words'): # bridge to the text corpus reader
        #     source = [source.words(f) for f in source.fileids()]
        #
        # self._texts = source
        # Text.__init__(self, LazyConcatenation(source))
        # self._idf_cache = {}

    def tf(self, term, text):
        # The frequency of the term in text.
        return text.count(term) / len(text)

    def df(self, term, text):
        return text.count(term)

    def idf(self, term, text):
        # The number of texts in the corpus divided by the number of texts that the term appears in.
        # idf values are cached for performance.
        # idf = self._idf_cache.get(term)
        # print(term, text)
        # print(len(self._texts),self.df(term, text))
        idf = log(len(self._texts) / (self.df(term, text) if self.df(term, text) != 0 else 1.0))
        # print(idf)
        return idf

    def tf_idf(self, term, text):
        return self.tf(term, text) * self.idf(term, text)


# reads the data from the file and returns the data and a text collection
def readInput(filename):
    fopen = open(filename, 'r', encoding='utf-8')
    data = fopen.readlines()
    fopen.close()
    return data


# generates the frequency profile for each class and returns it
def generate_fp(data1, data2):
    Class1FP = {}
    Class2FP = {}
    tc1 = MyTextCollection(data1)
    tc2 = MyTextCollection(data2)

    # tokenizing each line from the data and building a dictionary with line as key and tokens as values.
    for line in data1:
        l = Counter()
        l.update(word for word in word_tokenize(line.lower().strip()) if word not in stopw)
        Class1FP[line] = set(l)

    for line in data2:
        l = Counter()
        l.update(word for word in word_tokenize(line.lower().strip()) if word not in stopw)
        Class2FP[line] = set(l)
    # making a copy
    Class1FPCopy = Class1FP.copy()
    Class2FPCopy = Class2FP.copy()
    Class1FP = {}
    Class2FP = {}

    # giving global declarations
    global Class1P, Class2P

    # Probability that text belongs to either Class1 or Class2
    Class1P = len(data1) / (len(data1) + len(data2))
    Class2P = len(data2) / (len(data1) + len(data2))

    # Generating the frequency profiles for the class
    for line, tokens in Class1FPCopy.items():
        for token in tokens:
            if token not in Class1FP.keys():
                # tf-idf scoring for each token
                Class1FP[token] = tc1.tf_idf(token, line.strip().lower())
            else:
                Class1FP[token] += tc1.tf_idf(token, line.strip().lower())

    for line, tokens in Class2FPCopy.items():
        for token in tokens:
            if token not in Class2FP.keys():
                Class2FP[token] = tc2.tf_idf(token, line.strip().lower())
            else:
                Class2FP[token] += tc2.tf_idf(token, line.strip().lower())

    # Class1FP = Counter(dict([ (token, tc1.tf_idf(token,x)) for x,y in Class1FP.items() for token in y ]))
    # Class2FP = Counter(dict([ (token, tc2.tf_idf(token, x)) for x,y in Class2FP.items() for token in y]))
    return Class1FP, Class2FP


def predict(data, ClassFP, ClassP):
    totalClassTokens = sum(ClassFP.values()) + 1
    defaultClassP = 1 / totalClassTokens
    unknownText = ''

    # stripping and tokenizing
    for line in data:
        unknownText += line.strip()
    unknownTextTokens = word_tokenize(unknownText.lower())

    result = 0.0
    for token in unknownTextTokens:
        # print("Token: " + str(token))
        # print("Token Value: " + str(Class1FP.get(token)))
        # print(Class1FP.get(token))
        # print(log(Class1FP.get(token, defaultClassP)))
        try:
            result += log(Class1FP.get(token, defaultClassP), 2)
        except ValueError:
            result += log(defaultClassP, 2)
    result += log(ClassP)
    return result


def result(testDataPrediction_1, testDataPrediction_2):
    print(testDataPrediction_1, testDataPrediction_2)
    if max(testDataPrediction_1, testDataPrediction_2) == testDataPrediction_1:
        print("The text belongs to Class1")
    else:
        print("The text belongs to Class2")


if __name__ == "__main__":
    data1 = readInput(filename='input/input1.txt')
    data2 = readInput(filename='input/input2.txt')
    Class1FP, Class2FP = generate_fp(data1, data2)
    testData1 = readInput(filename='input/test1.txt')
    testData2 = readInput(filename='input/test2.txt')
    testData1Prediction_1 = predict(testData1, Class1FP, Class1P)
    testData1Prediction_2 = predict(testData1, Class2FP, Class2P)
    result(testData1Prediction_1, testData1Prediction_2)
    testData2Prediction_1 = predict(testData2, Class1FP, Class1P)
    testData2Prediction_2 = predict(testData2, Class2FP, Class2P)
    result(testData2Prediction_1, testData2Prediction_2)
