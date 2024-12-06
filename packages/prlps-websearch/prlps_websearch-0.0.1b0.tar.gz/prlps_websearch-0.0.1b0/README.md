`pip install prlps_websearch`


```python
from prlps_websearch import websearch
from asyncio import run as asyncio_run

async def main():
    result = await websearch(
        query='скачать книги бесплатно',  # str
        time_range='year',  # Literal['year', 'month', 'week', 'day']
        category='general',  # Literal['general', 'news', 'it', 'images', 'videos']
        num_pages=2  # int
    )
    print(result)

asyncio_run(main())
```
