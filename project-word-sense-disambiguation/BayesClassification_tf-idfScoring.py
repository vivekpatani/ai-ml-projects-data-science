"""Used tf-idf to calculate the scores for each token in our Frequency profile.
   However the issue with using tf-idf scoring for our current classification is that, assume that term driver appears
   in all five definitions, and therefore our idf score effectively becomes zero for that term, making it difficult to
   estimate"""

from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from math import log
from nltk.text import TextCollection

data1 = open('input\input1.txt', 'r').readlines()
data2 = open('input\input2.txt', 'r').readlines()

myTexts1 = TextCollection(data1)
myTexts2 = TextCollection(data2)

stopw = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')

Class1P = len(data1) / (len(data1) + len(data2))
Class2P = len(data2) / (len(data1) + len(data2))

Class1FP = {}
Class2FP = {}

for line in data1:
    l = Counter()
    l.update(word for word in tokenizer.tokenize(line.lower().strip()) if word not in stopw)
    Class1FP[line] = set(l)

for line in data2:
    l = Counter()
    l.update(word for word in tokenizer.tokenize(line.lower().strip()) if word not in stopw)
    Class2FP[line] = set(l)

Class1FPCopy = Class1FP.copy()
Class2FPCopy = Class2FP.copy()
Class1FP = {}
Class2FP = {}

for line, tokens in Class1FPCopy.items():
    for token in tokens:
        if token not in Class1FP.keys():
            Class1FP[token] = myTexts1.tf_idf(token, line)
        else:
            Class1FP[token] += myTexts1.tf_idf(token, line)

for line, tokens in Class2FPCopy.items():
    for token in tokens:
        if token not in Class2FP.keys():
            Class2FP[token] = myTexts2.tf_idf(token, line)
        else:
            Class2FP[token] += myTexts2.tf_idf(token, line)

# Class1FP = Counter(dict([ (token, myTexts1.tf_idf(token,x)) for x,y in Class1FP.items() for token in y ]))
# Class2FP = Counter(dict([ (token, myTexts2.tf_idf(token, x)) for x,y in Class2FP.items() for token in y]))

totalClass1FP = sum(Class1FP.values()) + 1
totalClass2FP = sum(Class2FP.values()) + 1

defaultClass1P = 1 / totalClass1FP
defaultClass2P = 1 / totalClass2FP
# print(defaultClass1P)

unknownTextLines1 = open('input/test1.txt', 'r').readlines()
unknownText1 = ''
for x in unknownTextLines1:
    unknownText1 += x.strip()
unknownTextTokens1 = tokenizer.tokenize(unknownText1.lower())

result1_1 = 0.0
for token in unknownTextTokens1:
    result1_1 += log(Class1FP.get(token, defaultClass1P), 2)
result1_1 += Class1P

result1_2 = 0.0
for token in unknownTextTokens1:
    result1_2 += log(Class2FP.get(token, defaultClass2P), 2)
result1_2 += Class2P

print(result1_1, result1_2)
if max(result1_1, result1_2) == result1_1:
    print("Class1")
else:
    print("Class2")

unknownTextLines_2 = open('input/test2.txt', 'r').readlines()
unknownText_2 = ''
for x in unknownTextLines_2:
    unknownText_2 += x.strip()
unknownTextTokens_2 = tokenizer.tokenize(unknownText_2.lower())

result2_1 = 0.0
for token in unknownTextTokens_2:
    result2_1 += log(Class1FP.get(token, defaultClass1P), 2)
result2_1 += Class1P

result2_2 = 0.0
for token in unknownTextTokens_2:
    result2_2 += log(Class2FP.get(token, defaultClass2P), 2)
result2_2 += Class2P

print(result2_1, result2_2)
if max(result2_1, result2_2) == result2_1:
    print("Class1")
else:
    print("Class2")