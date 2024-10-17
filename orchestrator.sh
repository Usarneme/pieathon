#!/bin/bash

# step 1 - scrape to get the new data
python3 scrape.py

# step 2 - normalize the data
python3 normalize.py

# step 3 - prepare the json for the word clouds
python3 urls_data_to_json.py
python3 article_words_to_json.py

# step 4 - push up the changes to the hosted web content
cd www/
surge --domain usarneme-hn.surge.sh
