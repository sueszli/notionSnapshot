# progress

currently when exporting pages directly through the notion app or the notion api as done in [notion4ever](https://github.com/merkulovdaniil/notion4ever/tree/main/notion4ever) leads to the loss of formatting data and in some cases even page content.

therefore the best way to recreate the original look of the pages is to simply scrape them with a webscraper.

<br><br>

### choosing a scraping library

the following libraries were considered because they are the most popular and well supported (for python as of march 2023):

-   playwright: https://playwright.dev/python/docs/intro
-   selenium: https://selenium-python.readthedocs.io/ ✅

usually when installing a web driver you have to download the driver and add it to your `$path`. this is inconvenient for the end user.

playwright mitigates this problem by downloading the driver automatically when you install the library with your operating system's package manager. but this is again inconvenient, as we want this tool to be as easy to use as possible.

but we managed to find a way to install selenium directly through pip by using the `webdriver_manager` library.

this makes selenium the best option for our use case and makes using python just as convenient as node.js for this project.

<br><br>

### building on top of similar projects

there are already a few tools that do something very similar to what we want to do. we should try to build on top of these tools instead of reinventing the wheel.

i did a lot of research (i really mean a lot - i spent like 2 full days on this) and found the following tools to have the best replication of the original styling:

-   loconotion: https://github.com/leoncvlt/loconotion/ (clearly the best option but it does not support all features - such as file attachments)
-   fruition: https://github.com/stephenou/fruitionsite/ (this one inspired locotion)

we should just continue where loconotion left off, because it is the best option although it is far from perfect.

we should make loconotion simpler and more opinionated such that the tools becomes more accessible to the average user.

<br><br>

### what's next?

i don't know if this project will ever get any traction but here are some ideas for the future:

-   [ ] support more blocks (ie. file attachmet types) with selenium actions (see: https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html)

-   [ ] make using it more convenient by writing a "github actions" script to automatically scrape and deploy pages after entering an url

<br><br><br>

# blocks supported by the current version

this list is based on the notion snapshot test page (see: `test.sh`)

### blocks

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

### pages

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
