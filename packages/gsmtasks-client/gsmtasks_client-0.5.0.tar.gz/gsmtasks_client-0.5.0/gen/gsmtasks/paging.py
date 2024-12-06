__all__ = (
    'iter_pages',
)

from typing import AsyncIterable, Awaitable, Callable, Iterable, Optional, ParamSpec, TypeVar

import httpx
from lapidary.runtime import iter_pages as _iter_pages


def next_link_cursor_extractor(response: tuple) -> Optional[str]:
    meta = response[1]
    next_link = get_next_link(meta.link)
    if not next_link:
        return
    return httpx.URL(next_link).params['cursor']


def get_next_link(link: Iterable[str]) -> Optional[str]:
    if not link:
        return None
    links_list = [parse_header_link(link) for link in link]
    next_link = [link for link in links_list if link['rel'] == 'next']
    if next_link:
        return next_link.pop()['url']


def parse_header_link(value: str) -> dict[str, str]:
    replace_chars = " '\""
    value = value.strip(replace_chars)
    if not value:
        return {}

    try:
        url, params = value.split(";", 1)
    except ValueError:
        url, params = value, ""
    link = {"url": url.strip("<> '\"")}
    for param in params.split(";"):
        try:
            key, value = param.split("=")
        except ValueError:
            break
        link[key.strip(replace_chars)] = value.strip(replace_chars)
    return link


P = ParamSpec('P')
R = TypeVar('R')


def iter_pages(fn: Callable[P, Awaitable[R]]) -> Callable[P, AsyncIterable[R]]:
    return _iter_pages(fn, 'cursor_q', next_link_cursor_extractor)
