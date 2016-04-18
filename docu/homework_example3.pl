
#Part 3
word_list = graphlab.text_analytics.count_words(sf['X2'])
sf['word_list'] = word_list
sf['tfidf'] = graphlab.text_analytics.tf_idf(sf['word_list'])