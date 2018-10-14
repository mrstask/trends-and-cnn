Supported Python version 3.7+

This is an asynchronous parser for Google Trends Realtime Search Trends, and finding coincidences in CNN RSS feeds.

Script has both parser and frontend UI. I used Pypeeter and Feedparser libraries for parser and Aiohttp server for the frontend. 

To get a result from the script you need to run client.py to parse the data.
All parsed data will be written to the result.txt file,
after this you need to run the server.py file to start the server, and you can see UI in your browser visiting http://127.0.0.1:8000 page