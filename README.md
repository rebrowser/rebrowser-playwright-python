# rebrowser-playwright
> ⚠️ This is the original [`playwright-python`](https://github.com/microsoft/playwright-python) patched with [`rebrowser-patches`](https://github.com/rebrowser/rebrowser-patches).
>
> 🕵️ The ultimate goal is to pass all automation detection tests presented in [`rebrowser-bot-detector`](https://github.com/rebrowser/rebrowser-bot-detector).
>
> 🪄 It's designed to be a drop-in replacement for the original `playwright` without changing your codebase. Each major and minor version of this repo matches the original repo, patch version could differ due to changes related to the patch itself.
>
> ☝️ Make sure to read: [How to Access Main Context Objects from Isolated Context](https://rebrowser.net/blog/how-to-access-main-context-objects-from-isolated-context-in-puppeteer-and-playwright-23741)
>
> 🐛 Please report any issues in the [`rebrowser-patches`](https://github.com/rebrowser/rebrowser-patches/issues) repo.

# 🎭 [Playwright](https://playwright.dev) for Python [![PyPI version](https://badge.fury.io/py/playwright.svg)](https://pypi.python.org/pypi/playwright/) [![Anaconda version](https://img.shields.io/conda/v/microsoft/playwright)](https://anaconda.org/Microsoft/playwright) [![Join Discord](https://img.shields.io/badge/join-discord-infomational)](https://aka.ms/playwright/discord)

Playwright is a Python library to automate [Chromium](https://www.chromium.org/Home), [Firefox](https://www.mozilla.org/en-US/firefox/new/) and [WebKit](https://webkit.org/) browsers with a single API. Playwright delivers automation that is **ever-green**, **capable**, **reliable** and **fast**. [See how Playwright is better](https://playwright.dev/python).

|          | Linux | macOS | Windows |
|   :---   | :---: | :---: | :---:   |
| Chromium <!-- GEN:chromium-version -->129.0.6668.29<!-- GEN:stop --> | ✅ | ✅ | ✅ |
| WebKit <!-- GEN:webkit-version -->18.0<!-- GEN:stop --> | ✅ | ✅ | ✅ |
| Firefox <!-- GEN:firefox-version -->130.0<!-- GEN:stop --> | ✅ | ✅ | ✅ |

## Documentation

[https://playwright.dev/python/docs/intro](https://playwright.dev/python/docs/intro)

## API Reference

[https://playwright.dev/python/docs/api/class-playwright](https://playwright.dev/python/docs/api/class-playwright)

## Example

```py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto('http://playwright.dev')
        page.screenshot(path=f'example-{browser_type.name}.png')
        browser.close()
```

```py
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch()
            page = await browser.new_page()
            await page.goto('http://playwright.dev')
            await page.screenshot(path=f'example-{browser_type.name}.png')
            await browser.close()

asyncio.run(main())
```

## Other languages

More comfortable in another programming language? [Playwright](https://playwright.dev) is also available in
- [Node.js (JavaScript / TypeScript)](https://playwright.dev/docs/intro),
- [.NET](https://playwright.dev/dotnet/docs/intro),
- [Java](https://playwright.dev/java/docs/intro).
