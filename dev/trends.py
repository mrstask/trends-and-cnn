import asyncio
from pyppeteer import launch
from pprint import pprint
import json

data = {}

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=e')
    await page.waitForXPath('//div[@class="feed-load-more-button"]')
    items = await page.querySelectorAll('div.feed-item-header')
    for idx, item in enumerate(items):
        titles = await item.querySelectorAll('div.title > span > a')
        my_list = []
        for title in titles:
            title = await page.evaluate('(title) => title.textContent', title)
            my_list.append(title.strip())
        article = await item.querySelector('div.summary-text > a')
        article = await page.evaluate('(article) => article.textContent', article)
        data[idx] = {'title': my_list, 'article': article}
        # print(data)
    print(len(items))
    pprint(data)
    # await page.screenshot({'path': 'example.png'})
    await browser.close()
    with open('trends.txt', 'w') as f:
        f.write(json.dumps(data))

asyncio.run(main())
