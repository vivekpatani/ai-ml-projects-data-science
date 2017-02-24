from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from math import log

stopw = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')


def readInputFiles(filename):
    fopen = open(filename, 'r', encoding='utf-8')
    data = fopen.readlines()
    fopen.close()
    return data


def generateFP(data1, data2):
    global totalClass1, Class1P
    global totalClass2, Class2P

    # Probability that text belongs to either Class1 or Class2
    Class1P = len(data1) / (len(data1) + len(data2))
    Class2P = len(data2) / (len(data1) + len(data2))

    Class1FP = Counter()
    Class2FP = Counter()

    for definition in data1:
        Class1FP.update(word for word in tokenizer.tokenize(definition.lower().strip()) if word not in stopw)

    for definition in data2:
        Class2FP.update(word for word in tokenizer.tokenize(definition.lower().strip()) if word not in stopw)

    # Note: We will be using tf scoring for our Frequency Profiles.
    totalClass1 = sum(Class1FP.values()) + 1
    totalClass2 = sum(Class2FP.values()) + 1

    Class1FP = Counter(dict([(token, frequency / totalClass1) for token, frequency in Class1FP.items()]))
    Class2FP = Counter(dict([(token, frequency / totalClass2) for token, frequency in Class2FP.items()]))

    # print(Class1FP,'/n/n','-'*100,'/n/n', Class2FP)

    return Class1FP, Class2FP


def predict(data, ClassFP, totalClassTokens, ClassP):
    defaultClassP = 1 / totalClassTokens
    result = 0.0
    resultTokens = []

    for line in data:
        resultTokens += tokenizer.tokenize(line.lower().strip())

    for token in resultTokens:
        result += log(ClassFP.get(token, defaultClassP), 2)
    result += log(ClassP)
    print(result)
    return result


def result(testDataPrediction_1, testDataPrediction_2):
    if max(testDataPrediction_1, testDataPrediction_2) == testDataPrediction_1:
        print("The test data file belongs to Input Class 1")
    else:
        print("The test data file belongs to Input Class 2")


if __name__ == "__main__":
    data1 = readInputFiles(filename='input/input1.txt')
    data2 = readInputFiles(filename='input/input2.txt')
    Class1FP, Class2FP = generateFP(data1, data2)
    testData1 = readInputFiles(filename='input/test1.txt')
    testData2 = readInputFiles(filename='input/test2.txt')
    testData1Prediction_1 = predict(testData1, Class1FP, totalClass1, Class1P)
    testData1Prediction_2 = predict(testData1, Class2FP, totalClass2, Class2P)
    result(testData1Prediction_1, testData1Prediction_2)
    testData2Prediction_1 = predict(testData2, Class1FP, totalClass1, Class1P)
    testData2Prediction_2 = predict(testData2, Class2FP, totalClass2, Class2P)
    result(testData1Prediction_1, testData1Prediction_2)