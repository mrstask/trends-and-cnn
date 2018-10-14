import jinja2
import aiohttp_jinja2
from aiohttp import web
import json


app = web.Application()


async def main(request):
    parsed_data = list()
    with open('result.txt') as f:
        data = f.read()
        for file in json.loads(data):
            print(file)
            print([file['title'], file['summary'], file['link'], file['published'], file['category']])
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

