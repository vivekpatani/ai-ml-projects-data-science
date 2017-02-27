from nltk import word_tokenize
from collections import Counter
from math import log


def readfile(filename, location="input/"):
    """
    Read the input files
    """
    file_data = open(location + filename).read()
    file_data = file_data.split('.')
    return file_data

def tokenise(text, meaning):
    """
    Tokenise the given text using NLTK
    """
    for each_item in text:
    	meaning.update(word_tokenize(each_item.lower()))
    return meaning

def main():

	# Reading Train Files
	print("Reading Train Files...")
	text1 = readfile("input1.txt")
	text2 = readfile("input2.txt")

	# Reading Train Files
	print("Reading Test Files...")
	test1 = readfile("test1.txt")
	test2 = readfile("test2.txt")

	profession = Counter()
	computer = Counter()

	# Tokenise the input
	print("Tokenising Train Files...")
	profession = tokenise(text1, profession)
	computer = tokenise(text2, computer)

	professiontest = Counter()
	computertest = Counter()

	# Tokenise Test Files
	print("Tokenising Test Files...")
	professiontest = tokenise(test1, computertest)
	computertest = tokenise(test2, professiontest)

	# Training Naive Bayes
	total = len(profession) + len(computer)

	computerprior = len(computer) / total
	professionprior = len(profession) / total

	totalcomputer = sum(computer.values()) + 1
	totalprofession = sum(profession.values()) + 1

	computer  = Counter( dict([ (token, frequency/totalcomputer)  for token, frequency in computer.items() ]) )
	profession = Counter( dict([ (token, frequency/totalprofession) for token, frequency in profession.items() ]) )

	defaultcomputer = 1 / totalcomputer
	defaultprofession  = 1 / totalprofession

	print("\nResult")
	# Testing Naive Bayes
	resultcomputer = log(computerprior)
	for each_item in computertest:
		resultcomputer += log(computer.get(each_item, defaultcomputer), 2)

	notresultcomputer = log(professionprior)
	for each_item in computertest:
		notresultcomputer += log(profession.get(each_item, defaultprofession), 2)

	if (resultcomputer > notresultcomputer): print("Correctly Classified Computer Driver Meaning")
	else: print("Incorrectly Classified Computer Driver Meaning")

	# Test 2
	resultprofession = log(professionprior)
	for each_item in professiontest:
		resultprofession += log(profession.get(each_item, defaultprofession), 2)

	notresultprofession = log(computerprior)
	for each_item in professiontest:
		notresultprofession += log(computer.get(each_item, defaultcomputer), 2)

	if (resultprofession > notresultprofession): print("Correctly Classified Profession as a Driver Meaning")
	else: print("Incorrectly Classified Profession as a Driver Meaning")

if __name__ == "__main__":
	main()