"""
This module is an entrypoint to AgentQL service
"""

from typing import Any, Coroutine, Union

from agentql.ext.playwright._network_monitor import PageActivityMonitor
from agentql.ext.playwright.async_api import Page
from agentql.ext.playwright.async_api._utils_async import (
    add_dom_change_listener_shared,
    add_request_event_listeners_for_page_monitor_shared,
    handle_page_crash,
)
from playwright.async_api import Page as _Page


async def wrap_async(page: Union[Coroutine[Any, Any, _Page], _Page]) -> Page:
    """
    Casts a Playwright Async `Page` object to an AgentQL `Page` type to get access to the AgentQL's querying API.
    See `agentql.ext.playwright.async_api.Page` for API details.
    """
    if isinstance(page, Coroutine):
        page = await page  # type: ignore

    page.on("crash", handle_page_crash)

    # pylint: disable=W0212
    # This is added to capture pages that have already navigated without calling `goto()`
    if page._page_monitor is None:
        page._page_monitor = PageActivityMonitor()
        await add_request_event_listeners_for_page_monitor_shared(page, page._page_monitor)

    await add_dom_change_listener_shared(page)
    return page  # type: ignore
