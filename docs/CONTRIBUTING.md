# Progress

### Choosing a strategy to download the content of a Notion page

There are two ways to download the content of a Notion page:

1. Using the official Notion.so API as done in [notion4ever](https://github.com/MerkulovDaniil/notion4ever/tree/main/notion4ever). Has the disadvantage that it does not include any formatting related data.

2. Scraping the HTML of the page.

<br><br>

### Choosing a scraping library

The following libraries were considered because they are the most popular and well supported (for Python as of March 2023):

-   Playwright: https://playwright.dev/python/docs/intro
-   Selenium: https://selenium-python.readthedocs.io/ ✅

Usually when installing a web driver you have to download the driver and add it to your `$PATH`. This is inconvenient for the end user.

Playwright mitigates this problem by downloading the driver automatically when you install the library with your operating system's package manager. But this is again inconvenient, as we want this tool to be as easy to use as possible.

(This sucks because Playwright is also a lot more performant than Selenium and supports async/await.)

But we managed to find a way to install Selenium directly through pip by using the `webdriver_manager` library.

This makes Selenium the best option for our use case and makes using Python just as convenient as Node.js for this project.

<br><br>

### Building on top of similar projects

There are already a few tools that do something very similar to what we want to do. We should try to build on top of these tools instead of reinventing the wheel.

I did a lot of research (I really mean a lot - I spent like 2 full days on this) and found the following tools to have the best replication of the original styling:

-   Loconotion: https://github.com/leoncvlt/loconotion/ (clearly the best option but it does not support all features - such as file attachments)
-   Fruition: https://github.com/stephenou/fruitionsite/ (this one inspired Locotion)

We should just continue where Loconotion left off, because it is the best option although it is far from perfect.

We should make loconotion simpler and more opinionated such that the tools becomes more accessible to the average user.

<br><br>

### What's next?

I don't know if this project will ever get any traction. I told a few people about it and made some posts on reddit - we will see.

But if this gets any attention, here are some ideas for the future:

-   [ ] support more blocks with selenium actions (see: https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html)

-   [ ] turn it into an accessible plug and play tool that can be used by anyone

    -   [ ] build simple gui with tkinter (see: https://github.com/stars/sueszli/lists/python-guis) + executables for windows and osx
    -   [ ] integrate into github actions such that people just need to enter their URL and immediately get a hosted version of the snapshot

<br><br><br>

# Blocks supported by the current version

This list is based on the notion snapshot test page (see: `test.sh`)

<br>

### Blocks

-   [x] basic blocks
-   [ ] media
    -   [ ] embedded video (mp4)
    -   [ ] embedded music (mp3) - calls notion api for a download
-   [ ] databases
    -   [ ] table view (glitches horizontally, doesn't link to subpages correctly)
    -   [ ] timeline view (works, but is too small)
-   [x] advanced blocks (buttons break, but we were removing all javascript on purpose)
-   [x] inlines
-   [ ] embeds
    -   [ ] embedded pdfs

<br>

### Pages

-   [x] comments
-   [x] serif page
-   [x] monoserif page
-   [x] small text page
-   [x] full width page
-   [x] board page
-   [ ] table page (glitches horizontally, doesn't link to subpages correctly)
-   [x] timeline page
-   [x] calendar page
-   [x] list page
-   [x] gallery page
