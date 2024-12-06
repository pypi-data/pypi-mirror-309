`pip install prlps_websearch`


```python
from prlps_websearch import async_websearch
from asyncio import run as asyncio_run

async def main():
    result = await async_websearch(
        query='скачать книги бесплатно',  # str
        time_range='year',  # Literal['year', 'month', 'week', 'day']
        category='general',  # Literal['general', 'news', 'it', 'images', 'videos']
        num_pages=2  # int
    )
    print(result)

asyncio_run(main())
```


```python
from prlps_websearch import sync_websearch

result = sync_websearch(
    query='скачать книги бесплатно',  # str
    time_range='year',  # Literal['year', 'month', 'week', 'day']
    category='general',  # Literal['general', 'news', 'it', 'images', 'videos']
    num_pages=2  # int
)
print(result)
```