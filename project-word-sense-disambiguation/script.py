from nltk import tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk import pos_tag

# Global Defs
stopw = stopwords.words("english")

def readfile(filename,location="input/"):
	"""
	Read the input files
	"""
	return open(location+filename).read()

def tokenise(text):
	"""
	Tokenises the given string using NLTK
	"""
	return tokenize.word_tokenize(text.lower())

def frequency_profile(tokens):
	"""
	Generates the count of each token
	"""
	print(Counter(tokens))
	return Counter(tokens)

def generate_model(fp):
	"""
	Generate a model readable by TimBL
	"""
	return [ (i, fp[i], len(i)) for i in fp ]

def pretty_print(model):
	"""
	Prints the model
	"""
	for item in model:
		print( "\t".join((str(item[1]), str(item[2]), str(isStopWord(item[0])) ) ))

def model_dump(model, filename, location="model/"):
	"""
	Dumps the model into a text file for TimBL
	"""
	with open(location + filename,'w') as output_dump:
		for item in model:
			output_dump.write(str(item[1]) + "\t" + str(item[2]) + "\t" + str(isStopWord(item[0])) + "\n")
	output_dump.close()

def isStopWord(word):
	"""
	1 is stopWord, 0 is not
	"""
	if (word in stopw):
		return 1
	return 0

def getPOSTokens(tokens):
	"""
	Tag each word with its token
	"""
	return [(x[0], x[1][0]) for x in pos_tag(tokens)]

def getUniquePOSTags(posTokens):
	"""
	Get All Unique POST Tags
	"""
	return list( set( [ x[1] for x in posTokens ] ) )

def main():
	"""
	Main
	"""

	# Reading the input file
	text1 = readfile("input1.txt")
	text2 = readfile("input2.txt")

	# Token Generation
	tokens1 = tokenise(text1)
	tokens2 = tokenise(text2)

	# Generating Frequency Profiles
	fp1 = frequency_profile(tokens1)
	fp2 = frequency_profile(tokens2)

	# Generate model
	model1 = generate_model(fp1)
	model2 = generate_model(fp2)

	# POS Tokens
	posTokens1 = getPOSTokens(tokens1)
	posTokens2 = getPOSTokens(tokens2)

	# Get Unique Tags
	getTags1 = getUniquePOSTags(posTokens1)
	getTags2 = getUniquePOSTags(posTokens2)

	# Pretty Tabular Prints for Model
	pretty_print(model1)
	pretty_print(model2)

	# Dump Model to output file
	model_dump(model1, "output1.txt")
	model_dump(model2, "output2.txt")

if __name__ == "__main__":
	main()