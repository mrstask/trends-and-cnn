import feedparser


with open('trends.txt', 'r') as f:
    trends_data = f.read().splitlines()
d = feedparser.parse('http://rss.cnn.com/rss/edition_entertainment.rss')
for entry in d['entries']:
    for item in trends_data:
        if item.lower() in entry['title'].lower():
            print(entry['title'])
            print(entry['summary'].split('<img')[0])

