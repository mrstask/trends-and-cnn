import feedparser
import asyncio
from pyppeteer import launch
import json

topics = {'business': ['http://rss.cnn.com/rss/money_news_international.rss',
                       'https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=b'],
          'sport': ['http://rss.cnn.com/rss/edition_sport.rss',
                    'https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=s'],
          'top': ['http://rss.cnn.com/rss/edition.rss',
                  'https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=h'
                  ],
          'world': ['http://rss.cnn.com/rss/edition_world.rss',
                    'https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all'],
          'most_resent': ['http://rss.cnn.com/rss/cnn_latest.rss',
                          'https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all'
                          ]
          }


async def trends_parse(cat_queue):
    cat_queue = await cat_queue.get()
    parsed_data = set()
    cat = cat_queue[0]
    browser = await launch()
    page = await browser.newPage()
    await page.goto(cat_queue[1])
    await page.waitForXPath('//div[@class="feed-load-more-button"]')
    items = await page.querySelectorAll('div.feed-item-header')

    for idx, title_item in enumerate(items):
        titles = await title_item.querySelectorAll('div.title > span > a')
        for title in titles:
            title = await page.evaluate('(title) => title.textContent', title)
            parsed_data.add(title.strip().lower())

    await browser.close()
    feed_parse([cat, list(parsed_data)], topics)
    return [cat, list(parsed_data)]


def feed_parse(trends_data, topic_urls):
    feed_url = topic_urls[trends_data[0]][0]
    d = feedparser.parse(feed_url)

    for entry in d['entries']:
        for item in trends_data[1]:
            if item.lower() in entry['title'].lower():
                parse_result = dict()
                parse_result['title'] = entry['title']
                parse_result['summary'] = entry['summary'].split('<img')[0]
                parse_result['link'] = entry['link']
                parse_result['published'] = entry['published']
                parse_result['category'] = trends_data[0]

                with open('result.txt', 'a') as f:
                    f.write(json.dumps(parse_result)+'\n')


async def main(topics_data):
    qu = asyncio.Queue()
    for key, value in topics_data.items():
        await qu.put([key, value[1]])

    tasks = []
    for _ in range(len(topics_data.keys())):
        task = asyncio.Task(trends_parse(qu))
        tasks.append(task)

    await asyncio.gather(*tasks)

asyncio.run(main(topics))
