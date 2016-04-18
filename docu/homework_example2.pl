
#Part 2
word_list = graphlab.text_analytics.count_words(sf['X2'])
docs = sf['word_list'].dict_trim_by_values(2)
docs = docs.dict_trim_by_keys(graphlab.text_analytics.stopwords(),exclude=True)