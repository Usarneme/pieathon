from logging_config import setup_logger
import os
import sqlite3

logger = setup_logger('urls_data_to_json.py')
logger.info('Starting urls_data_to_json.py...')

db_path = os.path.abspath('hackernews.sqlite')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('SELECT MAX(count) FROM Urls')
highest = cur.fetchone()[0] # take zeroeth item from the fetched tuple which corresponds to the number
cur.execute('SELECT MIN(count) FROM Urls')
lowest = cur.fetchone()[0]
bigsize = 80
smallsize = 20

fhand = open('www/urlsData.js','w')
fhand.write("urlsData = [")
first = True

cur.execute('SELECT * FROM Urls ORDER BY count DESC')
for record in cur:
    logger.info(f'Looping urls: {record}') # id, url, count
    if not first : fhand.write( ",\n")
    first = False
    url = record[1].replace('https://www.', '').replace('http://www.', '').replace('https://', '').replace('http://', '')
    count = record[2]
    size = (count - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("  {text: '"+url+"', size: "+str(size)+"}")

fhand.write( "\n];\n")
fhand.close()

logger.info('Finished writing urlsData json. Exiting urls_data_to_json.py...')
