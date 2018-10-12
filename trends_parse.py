import asyncio
from pyppeteer import launch


async def main():
    data = set()
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=e')
    await page.waitForXPath('//div[@class="feed-load-more-button"]')
    items = await page.querySelectorAll('div.feed-item-header')

    for idx, item in enumerate(items):
        titles = await item.querySelectorAll('div.title > span > a')
        for title in titles:
            title = await page.evaluate('(title) => title.textContent', title)
            data.add(title.strip().lower())

    await browser.close()
    with open('trends.txt', 'w') as f:
        for item in data:
            f.write(f'{item}\n')

asyncio.run(main())
