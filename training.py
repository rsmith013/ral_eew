from sklearn.neural_network import MLPClassifier
from urllib.parse import unquote
import json
import numpy as n
from datetime import datetime


def clean_query(query):
    """
    Remove characters we don't want and split the query on +
    :param query: Raw query
    :return: list of cleaned terms
    """

    return [unquote(term).strip('"./\\,)([]{}<>') for term in query.split('+')]


# Load lists of data
with open('output_data/data.json') as f:
    data = json.load(f)

# Initialise sets to create unique lists
individual_terms = set()
records = set()

# Add lower case search terms to set to get unique search terms
for item in (data['query']):
    individual_terms.update(clean_query(item))

# Create set of unique records
for item in data["extracted_hash"]:
    records.add(item)

# Turn unique terms and records into lists to preserve order
unique_words = list(individual_terms)
hash = list(records)

# Initialise the lists for the training set
training_set = []
output = []

# Loop through all the queries and create bag of words
query = data['query']
for x, y in zip(query, data['extracted_hash']):
    bag = []

    # Loop through all unique words add 1 if present else, 0.
    for word in unique_words:
        if word in clean_query(x):
            bag.append(1)
        else:
            bag.append(0)

    # Append record and bag to create training set and target
    training_set.append(bag)
    output.append(hash.index(y))

# sanity check to make sure we have same length input, output
print(len(training_set))
print(len(output))

# Retain a subset for validation
training_input = training_set[:3216]
training_output = output[:3216]
test_input = training_set[3216:]
test_output = output[3216:]

# Initialise hidden layer
hidden_layer = 100
new_score = 0
counter = 10

with open('output_data/hidden_layer_test.txt','w') as hidden_layer_output:

    while counter < 2000:
        start = datetime.now()
        clf = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(hidden_layer,), random_state=1)
        clf.fit(training_input, training_output)

        score = clf.score(test_input,test_output)

        hidden_layer_output.write("{},{}\n".format(hidden_layer,score))
        end = datetime.now() - start
        print ("Tested {} neurons. Score: {} Time: {}".format(hidden_layer, score, end))
        hidden_layer += 5

quit()

# Export model and save to disc
import pickle

with open('output_data/model.json', 'w') as outfile:
    outfile.write(pickle.dumps(clf))

quit()

while True:
    search = input("Please enter your search term(s): ")
    bag2 = []
    for word in unique_words:
        if word in search:
            bag2.append(1)
        elif search == "quit":
            break
        else:
            bag2.append(0)
    bag2 = n.array(bag2).reshape(1, -1)
    print(len(unique_words))
    predicted = clf.predict_proba(bag2)
    print(len(predicted[0]))
    sorted_probabilitys = sorted(predicted[0], reverse=True)
    for i in sorted_probabilitys[0:3]:
        print(hash[int(n.where(predicted[0] == i)[0])], i)

import pickle

with open('data.json', 'w') as outfile:
    outfile.write(pickle.dumps(clf))
