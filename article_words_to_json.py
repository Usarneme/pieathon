from logging_config import setup_logger
import os
import sqlite3

logger = setup_logger()
logger.info('Starting article_words_to_json.py...')

db_path = os.path.abspath('hackernews.sqlite')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('SELECT MAX(count) FROM Words')
highest = cur.fetchone()[0] # take zeroeth item from the fetched tuple which corresponds to the number
cur.execute('SELECT MIN(count) FROM Words')
lowest = cur.fetchone()[0]
bigsize = 80
smallsize = 20

fhand = open('www/wordsData.js','w')
fhand.write("wordsData = [")
first = True

cur.execute('SELECT * FROM Words ORDER BY count DESC')
for record in cur:
    logger.info(f'Looping Words: {record}') # id, word, count
    if not first : fhand.write( ",\n")
    first = False
    word = record[1]
    count = record[2]
    size = (count - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("  {text: '"+word+"', size: "+str(size)+"}")

fhand.write( "\n];\n")
fhand.close()

logger.info('Finished writing wordsData json. Exiting article_words_to_json.py...')
