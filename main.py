import feedparser
from trends_parse import data


d = feedparser.parse('http://rss.cnn.com/rss/edition_entertainment.rss')
for entry in d['entries']:
    for item in data:
        if item.lower() in entry['title'].lower():
            print(entry['title'])
            print(entry['summary'].split('<img')[0])
