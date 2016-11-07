###################################
# CS B551 Fall 2016, Assignment #3
#
# Your names and user ids: skariyat-sp60-vpatani-vsureshb
#
# (Based on skeleton code by D. Crandall)
#
#
####
"""
Problem Formulation:
In the initial step, conditional probability distribution tables for P(S1), P(S_i+1|S_i) and P(W_i|S_i) are calculated
in the following way
P(S1) - Probability for the number of sentences starting with the given POS (calcuated for all 12 POS tags)
P(S_i+1/S_i) - Probability for one POS tag followed by other  (12 x 12 combinations)
P(W_i/S_i) - Probability of each word in the training data for each POS tag (i.e, word/adj,word/adp,word/noun....etc)
Once these distributions are calculated, the test data can be tagged using the given models

1(b) Simple model:
The marginal probability distribution for each word of the sentence in test data is calculated given each
POS tag(12 tags in total). Then, the POS with maximum probability for that word will be assigned to it

1(a) Viterbi algorithm:
The best possible sequence is estimated using the calculated probability distributions given the words in the test data.
Once the final word of the sentence is tagged, backtracking is applied to estimate the POS tags for previous word

1(c) Complex model:
In this model, the probability distribution of each word is calculated given the probability distribution of 2 previous
words. Similar to simple model, but the max probability for the word in test data is calculated using variable
elimination based on the first previous tag as well as the tag previous to the first one.

Logarithm of posterior probability:
Log of posterior probability was calculated based on model 1(a). The result for each sentence is the log of
posterior calculated posterior probability for that sentence.

Assumptions:
If the word given the test data has not been estimated in the training data, then a smoothing parameter = 0.0000001
is assigned to the probability of that word given any POS tag.

So P(Unknown word|S_i) = 0.0000001

Accuracy:
The following results were obtained when the program was run for the bc.test training file

==> So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct:
   0. Ground truth:      100.00%              100.00%
     1. Simplified:       91.89%               38.15%
            2. HMM:       95.06%               54.45%
        3. Complex:       92.14%               40.85%
"""
####

from __future__ import division
from collections import defaultdict
import random
import math

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    pos_set = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'prt', 'verb', 'pron', 'x', '.']
    p_s1 = {}
    p_siplus_si = {}
    p_w_si = {}


    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    # log of posterior probability is calculated for model 1(a) using the example from piazza
    # P(noun, verb, adv, conj, noun, noun | Magnus ab integro seclorum nascitur ordo) = P(noun)P(verb|noun)P(magnus|noun)
    # P(adv|verb)P(ab|verb).......
    def posterior(self, sentence, label):
        previous_tag = ""
        log_post_prob = 1
        for word, pos in zip(sentence, label):
            if previous_tag == "":
                if word in Solver.p_w_si:
                    log_post_prob *= Solver.p_s1[pos] * Solver.p_w_si[word][pos]
                    previous_tag = pos
                else:
                    log_post_prob *= Solver.p_s1[pos] * 0.0000001
                    previous_tag = pos
            else:
                if word in Solver.p_w_si:
                    log_post_prob *= Solver.p_siplus_si[previous_tag][pos] * Solver.p_w_si[word][pos]
                    previous_tag = pos
                else:
                    log_post_prob *= Solver.p_s1[pos] * 0.0000001
                    previous_tag = pos
        return math.log(log_post_prob if log_post_prob > 0 else 1)



    # Calculate the possible initial probabilities of each POS tags P(S1), P(S2)......
    # Probabilities of each POS tag P(ADJ), P(DET), P(PRON)...... is calcualted
    def pos_probability(self, data):
        adj, adv, adp, conj, det, noun, num, pron, prt, verb, for_x, punc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        pos_map = {}

        for (s, gt) in data:
            if gt[0] == 'adj':
                adj += 1
            elif gt[0] == 'adv':
                adv += 1
            elif gt[0] == 'adp':
                adp += 1
            elif gt[0] == 'conj':
                conj += 1
            elif gt[0] == 'det':
                det += 1
            elif gt[0] == 'noun':
                noun += 1
            elif gt[0] == 'num':
                num += 1
            elif gt[0] == 'prt':
                prt += 1
            elif gt[0] == 'verb':
                verb += 1
            elif gt[0] == 'pron':
                pron += 1
            elif gt[0] == 'x':
                for_x += 1
            else:
                punc += 1

        pos_map['adj'] = adj / len(data)
        pos_map['adv'] = adv / len(data)
        pos_map['adp'] = adp / len(data)
        pos_map['conj'] = conj / len(data)
        pos_map['det'] = det / len(data)
        pos_map['noun'] = noun / len(data)
        pos_map['num'] = num / len(data)
        pos_map['prt'] = prt / len(data)
        pos_map['verb'] = verb / len(data)
        pos_map['pron'] = pron / len(data)
        pos_map['x'] = for_x / len(data)
        pos_map['.'] = punc / len(data)

        return pos_map

    # This method calculates the prob of given POS tag followed by another pos tag for all combinations
    # P(S_i+1|S_i)
    def siplus_si_prob(self,data):

        siplus_si_prob_map = {}

        # 12 X 12 combinations
        for pos in Solver.pos_set:
            siplus_si_prob_map[pos] = {}
            for pos_plus in Solver.pos_set:
                no_of_ot, total_out = 0, 0
                for (s, gt) in data:
                    for k in range(0, len(gt)):
                        if gt[k] == pos and k + 1 != len(gt):
                            if gt[k + 1] == pos_plus:
                                no_of_ot += 1
                                total_out += 1
                            else:
                                total_out += 1
                if total_out == 0:
                    siplus_si_prob_map[pos][pos_plus] = 0.0000001
                if total_out != 0:
                    siplus_si_prob_map[pos][pos_plus] = no_of_ot / total_out

        return siplus_si_prob_map

    # This method calculates the prob of each word given all the POS tags
    # ex: P('The'|ADJ), P('THE'|NOUN), P('THE'|PRON)..........
    def w_si(self,data):

        word_map = {}
        word_list =[]
        pos_list = []

        # create a list of words and pos tags
        for (s, gt) in data:
            word_list += s
            pos_list += gt

        # count the total number of tags
        pos_count = defaultdict(int)
        for tag in pos_list:
            pos_count[tag] += 1

        # count occurence of each word with pos tag
        word_pos_map = {}
        for f, b in zip(word_list, pos_list):
            if f not in word_pos_map:
                word_pos_map[f] = defaultdict(int)
            word_pos_map[f][b] += 1

        # compute wi_si
        for word in word_pos_map:
            if word not in word_map:
                word_map[word] = {}
            for tag in Solver.pos_set:
                word_map[word][tag] = word_pos_map[word][tag] / pos_count[tag]

        return word_map



    # Do the training!
    # This method estimates all the required conditional probability tables
    def train(self, data):

        Solver.p_s1 = self.pos_probability(data)
        Solver.p_siplus_si = self.siplus_si_prob(data)
        Solver.p_w_si = self.w_si(data)


    # Functions for each algorithm.
    # 1(b) Calculate Max Si|w for each word in the sentence
    def simplified(self, sentence):
        tagged_words = []
        score = []
        for word in sentence:
            temp_max = -1
            arg = ""
            for pos in Solver.pos_set:
                # Bayes formula
                if word in Solver.p_w_si:
                    numerator = Solver.p_w_si[word][pos] * Solver.p_s1[pos]
                    denominator = (Solver.p_w_si[word][pos] * Solver.p_s1[pos]) + ((1 - Solver.p_w_si[word][pos]) * (1 - Solver.p_s1[pos]))
                    p_si_w = numerator / denominator
                else:
                    p_si_w = 0.0000001  # smoothing parameter

                if p_si_w > temp_max:
                    temp_max = p_si_w
                    arg = pos

            tagged_words.append(arg)
            score.append(temp_max)

        return [ [tagged_words], [score] ]

    # 1(a) Viterbi algorithm
    # The previous state values v0[ADJ], v0[NOUN], v0[PRON]....are stored in the dictionary v_dict
    # Maximum probability select inside each v0[POS] is stored in another dictionary max_dict (used for backtracking)
    # Once the POS tag for final word is estimated, backtracking is done using max_dict to get the max_value chosen
    # in the previous vi[maxval{max_dict)].
    def hmm(self, sentence):
        v_dict = {}
        max_dict = {}
        tagged_words = []
        # get v0[ADJ], v0[NOUN], v0[PRON]..v1[ADJ], v1[NOUN], v1[PRON]...vlength of sent
        for i in range(0, len(sentence)):
            if not v_dict:
                v_dict[i] = {}
                for pos in Solver.pos_set:
                    if sentence[i] in Solver.p_w_si:
                        v_dict[i][pos] = Solver.p_s1[pos] * Solver.p_w_si[sentence[i]][pos]
                    else:
                        v_dict[i][pos] = Solver.p_s1[pos] * 0.0000001
            else:
                for pos_plus in Solver.pos_set:
                    max_list = []
                    if i not in max_dict:
                        max_dict[i] = {}
                    if i not in v_dict:
                        v_dict[i] = {}

                    for pos in Solver.pos_set:
                        max_list.append(v_dict[i - 1][pos] * Solver.p_siplus_si[pos][pos_plus])
                    if sentence[i] in Solver.p_w_si:
                        v_dict[i][pos_plus] = max(max_list) * Solver.p_w_si[sentence[i]][pos_plus]
                    else:
                        v_dict[i][pos_plus] = max(max_list) * 0.0000001
                    max_dict[i][pos_plus] = Solver.pos_set[(max_list.index(max(max_list)))]

        # check the last max value to start backtracking
        # All possible v0, v1, v2, ...vn would have been estimated in the previous step
        check_last_max = []
        for pos in Solver.pos_set:
            check_last_max.append(v_dict[len(sentence)-1][pos])

        max_value = Solver.pos_set[(check_last_max.index(max(check_last_max)))]
        tagged_words.insert(0, max_value)

        # Add each estimated tags in the tagged_words list
        for k in range(len(sentence)-1, 0, -1):
            max_value = max_dict[k][max_value]
            tagged_words.insert(0, max_value)

        return [ [tagged_words], [] ]

    # 1(c) variable elimination
    # For each given word the maximum probability is estimated based on the 2 previous states (POS tags in this case)
    # At each iteration one of the variables will be eliminated by marginalizing it out
    # if the sentence is of 3 words, word 1 will be estimated 1st, then word2|word1 and finally word3|word2, word1
    # basically the loop is iterated for all possible combinations to marginalize the given variable
    def complex(self, sentence):

        tagged_words = []
        score = []

        current_pos = ""

        for word in sentence:
            # if it is the first word in the sentence (i.e if it has no previous states)
            if current_pos == "":
                temp_max = -1
                arg = ""
                for pos in Solver.pos_set:
                    # Bayes formula
                    if word in Solver.p_w_si:
                        numerator = Solver.p_w_si[word][pos] * Solver.p_s1[pos]
                        denominator = (Solver.p_w_si[word][pos] * Solver.p_s1[pos]) + (
                        (1 - Solver.p_w_si[word][pos]) * (1 - Solver.p_s1[pos]))
                        p_si_w = numerator / denominator
                    else:
                        p_si_w = 0.0000001  # cannot be zero, need to figure out a smoothing algo

                    if p_si_w > temp_max:
                        temp_max = p_si_w
                        arg = pos

                score.append(temp_max)
                tagged_words.append(arg)
                current_pos = arg

            # if it has a previous state available
            else:
                temp_max = -1

                for pos in Solver.pos_set:
                    if word in Solver.p_w_si:
                        temp_prob = Solver.p_siplus_si[current_pos][pos] * Solver.p_w_si[word][pos] * Solver.p_s1[pos]
                    else:
                        temp_prob = Solver.p_siplus_si[current_pos][pos] * 0.0000001 * Solver.p_s1[pos]

                    if temp_prob > temp_max:
                        temp_max = temp_prob
                        arg = pos

                score.append(temp_max)
                tagged_words.append(arg)
                current_pos = arg

        return [[tagged_words], [score]]


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for simplified() and complex() and is the marginal probability for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM":
            return self.hmm(sentence)
        elif algo == "Complex":
            return self.complex(sentence)
        else:
            print "Unknown algo!"
