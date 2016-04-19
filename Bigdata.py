
# coding: utf-8

# In[7]:

import graphlab
import os
sf = graphlab.SFrame.read_csv('http://www.vivekpatani.tk/resources/reuters.csv', header=False)


# In[8]:

word_list = graphlab.text_analytics.count_words(sf['X2'])
sf['word_list'] = word_list
sf['tfidf'] = graphlab.text_analytics.tf_idf(sf['word_list'])
docs = sf['word_list'].dict_trim_by_values(2)
docs = docs.dict_trim_by_keys(graphlab.text_analytics.stopwords(), exclude=True)
docs[0]


# In[9]:

train_data, test_data = sf.random_split(0.8)


# In[10]:

model1 = graphlab.boosted_trees_classifier.create(train_data,target='X1',features=['tfidf'])
results1 = model1.evaluate(test_data)
predictions1 = model1.predict(test_data)
model1.show(view="Tree", tree_id=0)


# In[11]:

model2 = graphlab.nearest_neighbor_classifier.create(train_data[:10], target='X1')
results2 = model2.evaluate(test_data)
predictions2 = model2.classify(test_data[:1], max_neighbors=1, radius=None)
evals2 = model2.evaluate(test_data[:5])


# In[12]:

model3 = graphlab.decision_tree_classifier.create(train_data, target='X1',
                                           max_depth = 3)
results3 = model3.evaluate(test_data)
predictions3 = model3.predict(test_data)
model3.show(view="Tree", tree_id=0)


# In[13]:

model4 = graphlab.random_forest_classifier.create(train_data, target='X1',
                                           max_depth = 3)
results4 = model4.evaluate(test_data)
predictions4 = model4.predict(test_data)
model4.show(view="Tree", tree_id=0)


# In[14]:

from IPython.display import Image


# In[15]:

Image(url='http://www.vivekpatani.tk/resources/DecisionTree.PNG',embed=True)


# In[16]:

print("Excerpt of the tree fomed using Decision Tree, displaying distance/relevance between words.")


# In[17]:

Image(url='http://www.vivekpatani.tk/resources/BoostedTree.PNG',embed=True)


# In[18]:

print("Excerpt of the tree fomed using Boosted Tree, displaying distance/relevance between words.")


# In[19]:

Image(url='http://www.vivekpatani.tk/resources/relation1.png',embed=True)


# In[20]:

print("This displays the relevance between various wors, destination and source are the two words and the graph shows how relevant are they")


# In[21]:

Image(url='http://www.vivekpatani.tk/resources/relation2.png',embed=True)


# In[22]:

print("This displays the relevance between various wors, destination and source are the two words and the graph shows how relevant are they")


# In[23]:

results1


# In[24]:

results2


# In[25]:

results3


# In[26]:

results4


# In[28]:

evals2

