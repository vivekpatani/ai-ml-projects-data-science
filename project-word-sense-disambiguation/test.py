from nltk.corpus import wordnet as wn
from nltk.stem.porter import *
from subprocess import call

def readfile(filename,location="input/"):
    """
    Read the input files
    """
    file_data = open(location+filename).read()
    file_data = file_data.split('.')
    return file_data

def get_bag_of_words(word, important_meanings=[0, 1, 3]):
    """
    Returns a pre defined bag of words
    """
    bag = []
    bow = {"circuit" : [0, 4, 7],
            "device" : [0, 2],
            "virtual": [1],
            "vehicle": [0, 3],
            "driving": [1, 2, 3, 4, 17, 21, 24],
            "term"   : [0, 1, 3, 7],
            word     : important_meanings}
    
    for each in bow:
        bag.append(obtain_syns_anto(each, bow[each]))

    print(bag)
    return bag

def stem_word (word):
    """
    Stemming the word using
    PorterStemmer NLTK
    """
    ps = PorterStemmer()
    return ps.stem(word)

def print_meanings(word):
    """
    Using NLTK to obtain Syn Set
    """
    synsets = wn.synsets(word)
    print("Different Meanings:")
    for item in range(len(synsets)):
        print(str(item + 1) + ". " + str(synsets[item].definition()))
    print("\n")

def obtain_syns_anto(word, important_meanings):
    """
    Checking Synonms and Antonyms of the given word
    and returning if any
    """
    dis_similar = [word]

    # Stemming Going on
    word = stem_word(word)

    # Producing Syn Sets
    synsets = wn.synsets(word)

    # Going through synsets
    for item in range(len(synsets)):
        
        # We only care for these meanings of a given word
        if (item in important_meanings):
            # For each lemma
            for lemma in synsets[item].lemmas():
                dis_similar.append(lemma.name())
                if (lemma.antonyms()):
                    dis_similar.append(lemma.antonyms()[0].name())
    return set(dis_similar)

def fit(*args, vocabulary, class_label=0):
    """
    Accepts multiple datasets to prepare to provide
    input to TiMBL
    """
    if (len(args) == 0): return
    model = []
    class_label = 0

    for each_dataset in range(len(args)):
        for each_line in args[each_dataset]:
            line=[0] * len(vocabulary)
            for each_word in each_line.split():
                for bag in range(len(vocabulary)):
                    if each_word in vocabulary[bag]:
                        line[bag] = 1
            if (1 in line):
                model.append(line)
            line.append(class_label)
        class_label += 1

    return model

def dump_model (model, dir="model/", filename="output.txt"):
    """
    Dumps Model in a given file
    Which can be used for TiMBL
    """
    with open(dir + filename, 'w') as output:
        for vectors in model:
            for vector in vectors:
                output.write(str(vector) + "\t")
            output.write("\n")
    output.close()
    print("Dumping is over!")

def predict(test_data, vocabulary, class_label):
    test_model = fit(test_data, vocabulary=vocabulary, class_label=class_label)
    return test_model

def main():

    # Defining word to disambiguate
    ambiguous = "driver"
    print_meanings(ambiguous)

    # Get Bag of Words
    print("Reading Bag of Words...")
    bagofwords = get_bag_of_words(ambiguous)

    # Loading Train Files
    print("Loading Train Text...")
    train1 = readfile("input1.txt")
    train2 = readfile("input2.txt")

    # Loading Test Files
    print("Loading Test Text...")
    test1 = readfile("test1.txt")
    test2 = readfile("test2.txt")

    # Preparing Train Data
    print("Preparing Train Data...")
    model = fit(train1, train2, vocabulary=bagofwords)

    # Preparing Test Data
    print("Preparing Test Data...")
    # predict1 = predict(test1, bagofwords, 0)
    predict2 = predict(test2, bagofwords, 1)

    # Dumpping all models and Test Models
    dump_model(model, filename="model.txt")
    dump_model(predict2, filename="test_model.txt")

    # Training using TiMBL
    call(["timbl", "-f", "model/model.txt", "-t", "model/test_model.txt"])

if __name__ =="__main__":
    main()