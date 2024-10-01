# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from typing import Dict

import pytest
import requests

from playwright.async_api import BrowserType, Error
from tests.server import Server, WebSocketProtocol, find_free_port

pytestmark = pytest.mark.only_browser("chromium")


async def test_connect_to_an_existing_cdp_session(
    launch_arguments: Dict, browser_type: BrowserType
) -> None:
    port = find_free_port()
    browser_server = await browser_type.launch(
        **launch_arguments, args=[f"--remote-debugging-port={port}"]
    )
    cdp_browser = await browser_type.connect_over_cdp(f"http://127.0.0.1:{port}")
    assert len(cdp_browser.contexts) == 1
    await cdp_browser.close()
    await browser_server.close()


async def test_connect_to_an_existing_cdp_session_twice(
    launch_arguments: Dict, browser_type: BrowserType, server: Server
) -> None:
    port = find_free_port()
    browser_server = await browser_type.launch(
        **launch_arguments, args=[f"--remote-debugging-port={port}"]
    )
    endpoint_url = f"http://127.0.0.1:{port}"
    cdp_browser1 = await browser_type.connect_over_cdp(endpoint_url)
    cdp_browser2 = await browser_type.connect_over_cdp(endpoint_url)
    assert len(cdp_browser1.contexts) == 1
    page1 = await cdp_browser1.contexts[0].new_page()
    await page1.goto(server.EMPTY_PAGE)

    assert len(cdp_browser2.contexts) == 1
    page2 = await cdp_browser2.contexts[0].new_page()
    await page2.goto(server.EMPTY_PAGE)

    assert len(cdp_browser1.contexts[0].pages) == 2
    assert len(cdp_browser2.contexts[0].pages) == 2

    await cdp_browser1.close()
    await cdp_browser2.close()
    await browser_server.close()


def _ws_endpoint_from_url(url: str) -> str:
    response = requests.get(url)
    assert response.ok
    response_body = response.json()
    return response_body["webSocketDebuggerUrl"]


async def test_conect_over_a_ws_endpoint(
    launch_arguments: Dict, browser_type: BrowserType, server: Server
) -> None:
    port = find_free_port()
    browser_server = await browser_type.launch(
        **launch_arguments, args=[f"--remote-debugging-port={port}"]
    )
    ws_endpoint = _ws_endpoint_from_url(f"http://127.0.0.1:{port}/json/version/")

    cdp_browser1 = await browser_type.connect_over_cdp(ws_endpoint)
    assert len(cdp_browser1.contexts) == 1
    await cdp_browser1.close()

    cdp_browser2 = await browser_type.connect_over_cdp(ws_endpoint)
    assert len(cdp_browser2.contexts) == 1
    await cdp_browser2.close()
    await browser_server.close()


async def test_connect_over_cdp_passing_header_works(
    browser_type: BrowserType, server: Server
) -> None:
    server.send_on_web_socket_connection(b"incoming")
    request = asyncio.create_task(server.wait_for_request("/ws"))
    with pytest.raises(Error):
        await browser_type.connect_over_cdp(
            f"ws://127.0.0.1:{server.PORT}/ws", headers={"foo": "bar"}
        )
    assert (await request).getHeader("foo") == "bar"


async def test_should_print_custom_ws_close_error(
    browser_type: BrowserType, server: Server
) -> None:
    def _handle_ws(ws: WebSocketProtocol) -> None:
        def _onMessage(payload: bytes, isBinary: bool) -> None:
            ws.sendClose(code=4123, reason="Oh my!")

        setattr(ws, "onMessage", _onMessage)

    server.once_web_socket_connection(_handle_ws)
    with pytest.raises(Error, match="Browser logs:\n\nOh my!\n"):
        await browser_type.connect_over_cdp(
            f"ws://127.0.0.1:{server.PORT}/ws", headers={"foo": "bar"}
        )
