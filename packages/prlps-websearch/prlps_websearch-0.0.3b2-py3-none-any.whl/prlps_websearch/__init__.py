from asyncio import CancelledError, FIRST_COMPLETED, Task, all_tasks, create_task, gather, get_event_loop, new_event_loop, set_event_loop, wait, run as asyncio_run
from datetime import datetime, timedelta, timezone
from json import dumps, loads
from pathlib import Path
from random import choice
from tempfile import gettempdir
from typing import Any, Iterable, Literal
from urllib.parse import quote, urljoin

from httpx import AsyncClient, Timeout
from nest_asyncio import apply as nest_asyncio_apply
from parsel import Selector
from prlps_fakeua import random_headers

SEARX_URL = 'https://searx.space/data/instances.json'

SEARCH_PREFERENCES_ZLIB_BASE_64 = 'eJx1WMuO6zgO_ZrJxuigp28Dg1lk1cBsZ4DuvUFbjM1rWfTVI4nr65vyI6biO4sqlEmL4vPwuFqI2LEnDLcOHXqwFwuuS9DhDaw8cAsWbz5dIEVueZwsRrx1zJ3Fyx0e1LKrPQa2D_S3C41ysp48v-bbXz7hZcTYs7n9779__nUJcMeA4Nv-9usl9jjiLVC2eBEDycZQiy2HzzpCc_sP2IAXw3RYZ5DHK_vush6rQ5zFuezZpUUX0ddgqXOj_L3eDuYBrkVTb9euRn8k9HNNro4U5fwqJHcnR1GMtp6t3aTruexXu2ZqFlMW281-z3HAOdwM3kECuBgK0Fi5D11HTpL67w66umYJ1v_jtz_ATiKtLLn0qiZoB0lWqGuKWTcN1Ujes6_rO1kMi0yirOR3FSJ7VAoHkncD-1kfqZW_c_IXtX_Ro5ZICCX6LAhDXW8FlscnDTShIdDChizln7p-kEHOdpqpKd6Ihrru8IIndFKXgOrqMZu9tm17NagstT3eB5ZMvnPRWk7mbsEjkL6knSaPd_TZ8y08KUgIItQRiexpHiTNos7OOH08VqtjysEslB4TUf6dLSVvCQsXks_Xz1pmEL-kv-oxBWqX5xAhUjgCMqarpA9yExG7oA9nYxLv1kxaIVGQOWzkwhiIRV3WJhhhUnfhyN_3Cu6yKK01F3H886XivhvP-aq9eOKoiT3EUcZQv2apHbwWeMQq8D0-pVSVIS_Nn8dgLc3dkxsIdPPd51lF1CF99TJKWuIi83ZegMRIBxitX7ClrNEmmyzMeRzCEYbWjCwNEVTXjTKznsBWGaV0E_TQeMi_Njd6mUX065WrAF_v5hMj4Uq7x_1y4fZAo2kOz8mBuvw7hZ4P5SB5haA8tziOc5WCDNDx1iqcOMSTUMA3A5uWk0Th5ypXPJA2vSn4LqdcJwCqg89ajB5csBKabhgBpu5RNJ_lJkS8-j0vIwgSGXaffr_lPYQ-QqdVxu2HMUI7wfuRv_pi9Mfn2FgtcDPAEdUI0mq4l4zNHFBDTEYjkPbM8xMw5-lAi103pUb6G7YBLfUhSqdHmbPD9SyWQ6xSu6I2hbi5MZkGtaVJVoJsi7eJKY-p8nJ5vi4ocoDJRLnJGpjVPWxayakMae7EtzW_LdBqNaiTJbEJ5j42v348wUWtXgTlVHkwxFUjGBQ0tEkKDcXjUk9dHysDrM15jjEPsowYo6r26t44BypbK-BEsAPgOxuBkzPLJjiup7zInbSKvEoPDG3PsiV0jmXLtimE6zQLt9i7qQVj5msekiQIvOPTemPLBqv86y2VXpKVWf3EuMC6j1NmMcr7yMMsdZWBHnL77kUSXkJG0NCvc7mLYx40MQ2psKGkWwFiAR_JBYGx0OtlBT0XaZ85xdTotn9L9vw9aERWLzypmT-Xf8M8hE_hj8RlzbJQKuTbs3TCdoHa_yM-0pnFmSMsJSnffvD8keYn27uHUWhSX6CQoTZ-sSveHWfZXLKIqjeSmWL3ffv2r9dREpMMOt2lXw7Gwhx_RxzOkjOB2OTFJC2bZyLLamwcPPJUqZFJzdzhuEPphOg_armQJzk-ZGLzxEaXGUo-kp_PvvkkCKot2jxBglla9mRvHA2KdfCLBnaCHlWYHbs5M4IjVTj4MtpVdLp8Fe_AdMz49-k6PXXypWJtgU3h0WWYVbaEIcTMUHIG93MP4S8Ldd4S-JQPlF6S7NS53FejULAiVWkc7XzYkd34wGsRkazEY8d15cg18fed815kixT0HpyDUG1Ipeh5RuiV5WeHNrsNCNbBOB2j2si-LSm46855XaSFu4vklOiGYpOEx-yrSZYBCcwJnCljhjPTqfrU7G_JkfzTFUEf0rM_SnfyQekKj5X8ibnFVV0xziM7SRcWJJFSODLVyZca7C7Lw-F_hvUGfXfoEPIaOIq50LUjtI0xnsLa5KeQNvlPVgWNXdJUmZwcIk769MHd8loivSq_ftl4mqI49PrYhm7aI8lkRBgUsiYXeVdi0AV-U4SCG7x5wynsQ1UUTNjEmBFVMZt5Ik0uzqZW8RkAhPUNLGB4t_zcv1jDkJrkYto3cprQp_BmdxP9IunG0z5fFuJHawFZaaDM6YqtN1DxmgjyK0u69edWvkHY4PUUjVaeYtJKSCZ_HewV06qlrkd5nzH6K7kPKCoQYMGmMwQs4nNml-XcpzcZHbprxzsLPP4bMdkkeBVuudCv6_Z0zVR9U21M6dAx1Ou_Xp5eBuqkDmjvNbk7nzTChmr52G-HkyaXsZbPEWkEado3lP7ctxZsm2Spsz_Z6eXjSJb3tnKKu_3yGVfLB714PuaWuwhzE2p_-xsXLSX_'

Categories = Literal['general', 'news', 'it', 'images', 'videos']
TimeRanges = Literal['year', 'month', 'week', 'day']


def _is_writable_directory(path: str | Path) -> bool:
    directory = Path(path)
    if not directory.is_dir():
        return False
    try:
        test_file = directory / '.write_test'
        test_file.touch(exist_ok=False)
        test_file.unlink()
        return True
    except Exception:
        return False


def _is_recent(file_path: Path, hours: int = 12) -> bool:
    path = Path(file_path)
    if not path.exists():
        return False
    try:
        time_threshold = datetime.now(tz=timezone.utc) - timedelta(hours=hours)
        file_stat = path.stat()
        last_modified = datetime.fromtimestamp(file_stat.st_mtime, tz=timezone.utc)
        created_time = datetime.fromtimestamp(file_stat.st_ctime, tz=timezone.utc)
        return last_modified >= time_threshold or created_time >= time_threshold
    except:
        return False


def _get_path_for_data() -> Path:
    if _is_writable_directory(Path(__file__).parent):
        data_path = Path(__file__).parent.resolve()
    else:
        data_path = Path(gettempdir()).resolve()
    return data_path


SEARX_URLS_LIST_PATH = _get_path_for_data() / 'searx_urls.json'


class Cache:
    def __init__(self, expire: timedelta):
        self.expire = expire
        self.cache = {}
        self.timestamp = datetime.now()

    async def get(self, key):
        if datetime.now() - self.timestamp > self.expire:
            self.cache.clear()
            self.timestamp = datetime.now()
        return self.cache.get(key)

    async def set(self, key, value):
        self.cache[key] = value


cache = Cache(expire=timedelta(hours=12))


def _cache_results(func):
    async def wrapper(*args, **kwargs):
        cache_key = f"{func.__name__}:{args}:{kwargs}"
        cached_result = await cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        result = await func(*args, **kwargs)
        await cache.set(cache_key, result)
        return result

    return wrapper


def _search_results(html_content) -> list[dict[str, str]]:
    selector = Selector(html_content)
    results = []
    for article in selector.css('article.result'):
        url = article.css('a.url_header::attr(href)').get()
        snippet = article.xpath('string(p[@class="content"])').get()
        if url and snippet:
            results.append({'url': url, 'snippet': snippet.strip()})
    return results


def _parse_search_urls(json_text_content: str) -> list[str]:
    searx_instances = []
    response = loads(json_text_content)
    instances = response.get('instances')
    if instances:
        for url_key, params_value in instances.items():
            if params_value.get('network_type') == 'normal' and params_value.get('http', {}).get('status_code') == 200:
                searx_instances.append(url_key)
    return searx_instances


def _get_httpx_client():
    return AsyncClient(follow_redirects=True, timeout=Timeout(connect=5, read=10, write=10, pool=30))


async def _get_request(url: str, httpx_client: AsyncClient) -> str:
    headers = random_headers(url)
    headers.update({'Accept-Encoding': 'gzip'})
    try:
        response = await httpx_client.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except:
        return ''


async def _test_search_url(url: str, httpx_client: AsyncClient) -> bool:
    test_queries = ['чайный гриб', 'мурмурация', 'ректальный пролапс', 'дневник кающегося', 'гей порно', 'содержание серых жаб']
    try:
        await _search(url, httpx_client, choice(test_queries))
        return True
    except Exception as exc:
        return False


@_cache_results
async def _get_search_urls(httpx_client: AsyncClient) -> list[str]:
    if SEARX_URLS_LIST_PATH.is_file() and _is_recent(SEARX_URLS_LIST_PATH):
        content = SEARX_URLS_LIST_PATH.read_text()
        try:
            urls_list = loads(content)
            if urls_list:
                return urls_list
        except:
            pass
    response = await _get_request(SEARX_URL, httpx_client)
    url_list = _parse_search_urls(response)
    tasks = [_test_search_url(url, httpx_client) for url in url_list]
    test_results = await gather(*tasks)
    good_urls = [url for url, is_good in zip(url_list, test_results) if is_good]
    SEARX_URLS_LIST_PATH.write_text(dumps(good_urls))
    return loads(SEARX_URLS_LIST_PATH.read_text())


def _format_url(
        url: str,
        query: str,
        time_range: TimeRanges | None = None,
        category: Categories = 'general',
        num_pages: int = 1) -> Iterable[str]:
    return (
        urljoin(url, f'search?preferences={SEARCH_PREFERENCES_ZLIB_BASE_64}') +
        f'&q={quote(query)}' +
        f'&categories={category}' +
        f'&time_range={time_range}' +
        f'&pageno={i}' for i in range(1, max(1, min((int(num_pages), 10))) + 1)
    )


async def _search(
        url: str,
        httpx_client: AsyncClient,
        query: str,
        time_range: TimeRanges | None = None,
        category: Categories = 'general',
        num_pages: int = 1) -> dict[str, list[dict[str, str]] | str] | None:
    resp_urls = _format_url(url, query, time_range, category, num_pages)
    tasks = [_get_request(resp_url, httpx_client) for resp_url in resp_urls]
    html_contents = await gather(*tasks, return_exceptions=True)
    results_list = []
    for html_content in html_contents:
        if isinstance(html_content, str):
            results_list.extend(_search_results(html_content))
    return {'query': query, 'results': results_list} if results_list else None


async def _return_first_successful_task(tasks: list[Task]) -> Any | None:
    while tasks:
        done, pending = await wait(tasks, return_when=FIRST_COMPLETED)
        for task in done:
            if task.cancelled():
                continue
            try:
                result = await task
                if result is not None:
                    for pending_task in pending:
                        pending_task.cancel()
                    return result
            except CancelledError:
                continue
            except Exception as exc:
                continue
        tasks = list(pending)
    return None


async def async_websearch(
        query: str,
        time_range: TimeRanges | None = None,
        category: Categories = 'general',
        num_pages: int = 1) -> dict[str, list[dict[str, str]] | str] | None:
    """асинхронная функция для веб-поиска по заданному запросу.

    Args:
        query: строка поискового запроса.
        time_range: временной диапазон для поиска.
            может принимать значения 'year', 'month', 'week', 'day' или None (без ограничения по времени).
        category: категория поиска.
            может принимать значения 'general', 'news', 'it', 'images', 'videos'.
        num_pages: количество страниц результатов поиска для извлечения.

    Returns:
        словарь, содержащий запрос и список результатов. каждый результат представлен словарем
        с ключами 'url' (URL результата) и 'snippet' (фрагмент текста со страницы).
        например:
        ```
        {
            'query': 'скачать книги бесплатно',
            'results': [
                {'url': 'http://example.com/book1', 'snippet': 'Описание книги 1'},
                {'url': 'http://site.com/book2', 'snippet': 'Описание книги 2'},
                ...
            ]
        }
        ```
        если ни один из поисков не увенчался успехом, возвращается None.

    Raises:
        httpx.HTTPError: если возникла ошибка HTTP при выполнении запроса.

    Example:
        ```python
        from asyncio import run as asyncio_run

        async def main():
            result = await websearch(
                query='скачать книги бесплатно',
                time_range='year',
                category='general',
                num_pages=2
            )
            print(result)

        asyncio_run(main())
        ```
    """
    async with _get_httpx_client() as httpx_client:
        urls = await _get_search_urls(httpx_client)
        tasks = [create_task(_search(url, httpx_client, query, time_range, category, num_pages)) for url in urls]
        result = await _return_first_successful_task(tasks)
        return result


def sync_websearch(
        query: str,
        time_range: TimeRanges | None = None,
        category: Categories = 'general',
        num_pages: int = 1) -> dict[str, list[dict[str, str]] | str] | None:
    """синхронная функция для веб-поиска по заданному запросу.

    Args:
        query: строка поискового запроса.
        time_range: временной диапазон для поиска.
            может принимать значения 'year', 'month', 'week', 'day' или None (без ограничения по времени).
        category: категория поиска.
            может принимать значения 'general', 'news', 'it', 'images', 'videos'.
        num_pages: количество страниц результатов поиска для извлечения.

    Returns:
        словарь, содержащий запрос и список результатов. каждый результат представлен словарем
        с ключами 'url' (URL результата) и 'snippet' (фрагмент текста со страницы).
        например:
        ```
        {
            'query': 'скачать книги бесплатно',
            'results': [
                {'url': 'http://example.com/book1', 'snippet': 'Описание книги 1'},
                {'url': 'http://site.com/book2', 'snippet': 'Описание книги 2'},
                ...
            ]
        }
        ```
        если ни один из поисков не увенчался успехом, возвращается None.

    Raises:
        httpx.HTTPError: если возникла ошибка HTTP при выполнении запроса.

    Example:
        ```python
        from asyncio import run as asyncio_run

        async def main():
            result = await websearch(
                query='скачать книги бесплатно',
                time_range='year',
                category='general',
                num_pages=2
            )
            print(result)

        asyncio_run(main())
        ```
    """
    try:
        nest_asyncio_apply()
        loop = get_event_loop()
        if loop.is_running():
            new_loop = new_event_loop()
            set_event_loop(new_loop)
            result = new_loop.run_until_complete(async_websearch(query, time_range, category, num_pages))
            for task in all_tasks(new_loop):
                task.cancel()
            new_loop.run_until_complete(new_loop.shutdown_asyncgens())
            new_loop.close()
        else:
            result = loop.run_until_complete(async_websearch(query, time_range, category, num_pages))
            for task in all_tasks(loop):
                task.cancel()
            loop.run_until_complete(loop.shutdown_asyncgens())
        return result
    except:
        try:
            return asyncio_run(async_websearch(query, time_range, category, num_pages))
        except:
            return None
