import jinja2
import aiohttp_jinja2
from aiohttp import web
import feedparser
from pyppeteer import launch

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


app = web.Application()


async def trends_parse(topics_items):
    result = list()
    browser = await launch()
    page = await browser.newPage()
    for cat, urls in topics_items.items():
        parsed_data = set()
        await page.goto(urls[1])
        await page.waitForXPath('//div[@class="feed-load-more-button"]')
        items = await page.querySelectorAll('div.feed-item-header')

        for idx, title_item in enumerate(items):
            titles = await title_item.querySelectorAll('div.title > span > a')
            for title in titles:
                title = await page.evaluate('(title) => title.textContent', title)
                parsed_data.add(title.strip().lower())
        rss_result = feed_parse([cat, list(parsed_data)], topics)

        if rss_result:
            for item in rss_result:
                if item not in result:
                    result.append(item)

    await browser.close()
    return result


def feed_parse(trends_data, topic_urls):
    feed_url = topic_urls[trends_data[0]][0]
    d = feedparser.parse(feed_url)
    all_results = list()
    for entry in d['entries']:
        for item in trends_data[1]:
            if item.lower() in entry['title'].lower():
                parse_result = dict()
                parse_result['title'] = entry['title']
                try:
                    parse_result['summary'] = entry['summary'].split('<img')[0]
                except KeyError:
                    parse_result['summary'] = 'No Summary'
                parse_result['link'] = entry['link']
                parse_result['published'] = entry['published']
                parse_result['category'] = trends_data[0]
                all_results.append(parse_result)
    return all_results


async def main(request):
    result = await trends_parse(topics)
    parsed_data = list()
    for file in result:
        parsed_data.append([file['title'], file['summary'], file['link'], file['published'], file['category']])
    context = {'data': parsed_data}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    return response


app = web.Application()

app.add_routes([web.get('/', main)])

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static', 'static', name='static')
jenv = app.get('aiohttp_jinja2_environment')

web.run_app(app, host='127.0.0.1', port=8000)

