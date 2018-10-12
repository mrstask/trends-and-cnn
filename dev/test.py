import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=e')
    await page.waitForXPath('//div[@class="feed-load-more-button"]')
    items = await page.querySelectorAll('div.feed-item-header')
    for item in items:
            titles = await item.querySelectorAll('div.title > span > a')
            for title in titles:
                title = await page.evaluate('(title) => title.textContent', title)
                print(title.strip())
            article = await item.querySelector('div.summary-text > a')
            article = await page.evaluate('(article) => article.textContent', article)
            print(article)
            print('*'*50)
    print(len(items))
    # await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.run(main())