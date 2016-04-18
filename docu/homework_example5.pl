model = graphlab.boosted_trees_classifier.create(train_data, target='X1',
                                           max_iterations=2,
                                           max_depth = 3)
predictions = model.classify(test_data)
results = model.evaluate(test_data)