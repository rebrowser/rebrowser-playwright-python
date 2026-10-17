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

"""
Python package `playwright` is a Python library to automate Chromium,
Firefox and WebKit with a single API. Playwright is built to enable cross-browser
web automation that is ever-green, capable, reliable and fast.
"""

from typing import Any, Optional, Union, overload

import rebrowser_playwright._impl._api_structures
import rebrowser_playwright._impl._errors
import rebrowser_playwright._impl._form_data
import rebrowser_playwright.async_api._generated
from rebrowser_playwright._impl._assertions import (
    APIResponseAssertions as APIResponseAssertionsImpl,
)
from rebrowser_playwright._impl._assertions import LocatorAssertions as LocatorAssertionsImpl
from rebrowser_playwright._impl._assertions import PageAssertions as PageAssertionsImpl
from rebrowser_playwright.async_api._context_manager import PlaywrightContextManager
from rebrowser_playwright.async_api._generated import (
    APIRequest,
    APIRequestContext,
    APIResponse,
    APIResponseAssertions,
    Browser,
    BrowserContext,
    BrowserType,
    CDPSession,
    ConsoleMessage,
    Dialog,
    Download,
    ElementHandle,
    FileChooser,
    Frame,
    FrameLocator,
    JSHandle,
    Keyboard,
    Locator,
    LocatorAssertions,
    Mouse,
    Page,
    PageAssertions,
    Playwright,
    Request,
    Response,
    Route,
    Selectors,
    Touchscreen,
    Video,
    WebError,
    WebSocket,
    WebSocketRoute,
    Worker,
)

ChromiumBrowserContext = BrowserContext

Cookie = rebrowser_playwright._impl._api_structures.Cookie
FilePayload = rebrowser_playwright._impl._api_structures.FilePayload
FormData = rebrowser_playwright._impl._form_data.FormData
FloatRect = rebrowser_playwright._impl._api_structures.FloatRect
Geolocation = rebrowser_playwright._impl._api_structures.Geolocation
HttpCredentials = rebrowser_playwright._impl._api_structures.HttpCredentials
BrowserBindResult = rebrowser_playwright._impl._api_structures.BrowserBindResult
DebuggerLocation = rebrowser_playwright._impl._api_structures.DebuggerLocation
DebuggerPausedDetails = rebrowser_playwright._impl._api_structures.DebuggerPausedDetails
PdfMargins = rebrowser_playwright._impl._api_structures.PdfMargins
Position = rebrowser_playwright._impl._api_structures.Position
ProxySettings = rebrowser_playwright._impl._api_structures.ProxySettings
ResourceTiming = rebrowser_playwright._impl._api_structures.ResourceTiming
ScreencastActionStyle = rebrowser_playwright._impl._api_structures.ScreencastActionStyle
ScreencastFrame = rebrowser_playwright._impl._api_structures.ScreencastFrame
ScreencastSize = rebrowser_playwright._impl._api_structures.ScreencastSize
SourceLocation = rebrowser_playwright._impl._api_structures.SourceLocation
StorageState = rebrowser_playwright._impl._api_structures.StorageState
StorageStateCookie = rebrowser_playwright._impl._api_structures.StorageStateCookie
ViewportSize = rebrowser_playwright._impl._api_structures.ViewportSize
VirtualCredential = rebrowser_playwright._impl._api_structures.VirtualCredential
WebMCPTool = rebrowser_playwright._impl._api_structures.WebMCPTool
WebMCPToolAnnotations = rebrowser_playwright._impl._api_structures.WebMCPToolAnnotations

Error = rebrowser_playwright._impl._errors.Error
TimeoutError = rebrowser_playwright._impl._errors.TimeoutError


def async_playwright() -> PlaywrightContextManager:
    return PlaywrightContextManager()


class Expect:
    _unset: Any = object()

    def __init__(self) -> None:
        self._timeout: Optional[float] = None

    def set_options(self, timeout: Optional[float] = _unset) -> None:
        """
        This method sets global `expect()` options.

        Args:
            timeout (float): Timeout value in milliseconds. Default to 5000 milliseconds.

        Returns:
            None
        """
        if timeout is not self._unset:
            self._timeout = timeout

    @overload
    def __call__(
        self, actual: Page, message: Optional[str] = None
    ) -> PageAssertions: ...

    @overload
    def __call__(
        self, actual: Locator, message: Optional[str] = None
    ) -> LocatorAssertions: ...

    @overload
    def __call__(
        self, actual: APIResponse, message: Optional[str] = None
    ) -> APIResponseAssertions: ...

    def __call__(
        self, actual: Union[Page, Locator, APIResponse], message: Optional[str] = None
    ) -> Union[PageAssertions, LocatorAssertions, APIResponseAssertions]:
        return self._dispatch(actual, message, is_soft=False)

    @overload
    def soft(self, actual: Page, message: Optional[str] = None) -> PageAssertions: ...

    @overload
    def soft(
        self, actual: Locator, message: Optional[str] = None
    ) -> LocatorAssertions: ...

    @overload
    def soft(
        self, actual: APIResponse, message: Optional[str] = None
    ) -> APIResponseAssertions: ...

    def soft(
        self, actual: Union[Page, Locator, APIResponse], message: Optional[str] = None
    ) -> Union[PageAssertions, LocatorAssertions, APIResponseAssertions]:
        """
        Creates a [soft assertion](https://playwright.dev/python/docs/test-assertions#soft-assertions).
        Failing soft assertions do not abort test execution, but mark the test
        as failed. Multiple failures from the same test are surfaced together
        at the end of the test.

        Requires the [pytest-playwright](https://pypi.org/project/pytest-playwright/)
        plugin to establish the per-test scope that collects soft assertion
        failures.
        """
        return self._dispatch(actual, message, is_soft=True)

    def _dispatch(
        self,
        actual: Union[Page, Locator, APIResponse],
        message: Optional[str],
        is_soft: bool,
    ) -> Union[PageAssertions, LocatorAssertions, APIResponseAssertions]:
        if isinstance(actual, Page):
            return PageAssertions(
                PageAssertionsImpl(
                    actual._impl_obj,
                    self._timeout,
                    message=message,
                    is_soft=is_soft,
                )
            )
        elif isinstance(actual, Locator):
            return LocatorAssertions(
                LocatorAssertionsImpl(
                    actual._impl_obj,
                    self._timeout,
                    message=message,
                    is_soft=is_soft,
                )
            )
        elif isinstance(actual, APIResponse):
            return APIResponseAssertions(
                APIResponseAssertionsImpl(
                    actual._impl_obj,
                    self._timeout,
                    message=message,
                    is_soft=is_soft,
                )
            )
        raise ValueError(f"Unsupported type: {type(actual)}")


expect = Expect()


__all__ = [
    "expect",
    "async_playwright",
    "APIRequest",
    "APIRequestContext",
    "APIResponse",
    "Browser",
    "BrowserBindResult",
    "BrowserContext",
    "BrowserType",
    "CDPSession",
    "ChromiumBrowserContext",
    "ConsoleMessage",
    "Cookie",
    "Dialog",
    "Download",
    "ElementHandle",
    "Error",
    "FileChooser",
    "FilePayload",
    "FloatRect",
    "FormData",
    "Frame",
    "FrameLocator",
    "Geolocation",
    "HttpCredentials",
    "JSHandle",
    "Keyboard",
    "Locator",
    "Mouse",
    "DebuggerLocation",
    "DebuggerPausedDetails",
    "Page",
    "PdfMargins",
    "Position",
    "Playwright",
    "ProxySettings",
    "Request",
    "ResourceTiming",
    "Response",
    "Route",
    "ScreencastActionStyle",
    "ScreencastFrame",
    "ScreencastSize",
    "Selectors",
    "SourceLocation",
    "StorageState",
    "StorageStateCookie",
    "TimeoutError",
    "Touchscreen",
    "Video",
    "ViewportSize",
    "VirtualCredential",
    "WebError",
    "WebMCPTool",
    "WebMCPToolAnnotations",
    "WebSocket",
    "WebSocketRoute",
    "Worker",
]
