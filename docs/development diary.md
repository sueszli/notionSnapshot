This is a collection of notes and considerations that were made during the development of the project.

<br><br>

## Choosing a strategy to download the content of a Notion page: Scraping

There are 3 ways to download the content of a Notion page:

1. Using the website's HTML feature
  This sucks - it is the very thing we are trying to avoid.
 
2. Using the official Notion.so API
  As done in [notion4ever](https://github.com/MerkulovDaniil/notion4ever/tree/main/notion4ever): The user would need to generate a token / API key and it would be significantly more complicated to set up for each page. 

3. Scraping the HTML files directly from the browser
  This is the best option because the user does not have to do any extra work to get the app to work - but it is also the most complicated option.

<br><br>

## Choosing a scraping library: Selenium

The following libraries were considered because they are the most popular and well supported (for Python as of March 2023):

- Playwright: https://playwright.dev/python/docs/intro
- Selenium: https://selenium-python.readthedocs.io/

Usually when installing a web driver you have to download the driver and add it to your `$PATH`. This is not ideal because it means that the user has to do extra work to get the app to work and you can not easily distribute the app as a single executable / dependency on a package manager.

Playwright has a built in driver manager which means that the user does not have to do any extra work to get the app to work. This is a big advantage over Selenium. But at the same time it has external dependencies that can not only installed with `pip` but also require the user to install other binaries.

This sucks because Playwright is also a lot more performant than Selenium.

But we managed to find a way to install Selenium with `pip` by using the `webdriver_manager` library. This means that we can use Selenium and the user does not have to do any extra work to get the app to work except having Python installed and running `pip`.

<br><br>

## Building on top of similar projects: Loconotion

There are already a few tools that do something very similar to what we want to do. We should try to build on top of these tools instead of reinventing the wheel.

I did a lot of research (really, I mean like 2 entire days) and found the following tools to have the best replication of the original styling:

- Loconotion: https://github.com/leoncvlt/loconotion/ (clearly the best option but it does not support all features - such as file attachments)
- Fruition: https://github.com/stephenou/fruitionsite/ (this one inspired Locotion)

<br>

We should just continue where Loconotion left off, because it is the best option.

We should make loconotion simpler and more opinionated by:

  - getting rid of the config `.toml` file and instead just offering a very minimal CLI interface
  - simplifying the installation process &rarr; ideally the user should be able to install the tool with a single command

and then we can add all the features that we want.

<br><br>

## Procedual style instead of OOP

I decided to write this script in a procedural style.
This is a very opinionated decision and I am open to changing it if it turns out to be a bad idea.

I still am using classes, but for a different purpose:

- classes only serve to bundle functions together, not to create multiple instances of the same class. if we need an object, we just create a singleton that gets passed to other modules
- only class variables but no instance variables to avoid writing getters and setters (really dangerous - but I think it is fine for a small script like this), alternatively we 

This would obviously be a total catastrophe if the project was bigger (which I don't think it will be) because it makes it a lot harder to trace side-effects on a more granular level (function, class - level, not just modules).

But for a small script like this it is fine and it makes the code a lot easier to read. We can always refactor it later if we want to.

<br><br>

## What's next?

I don't know if this project will ever get any traction, but if it does, here are some ideas for the future:


- [ ] support more blocks
  - [ ] all kinds of file attachments with selenium actions (see: https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html)

- [ ] make it more accessible for people who don't code / don't have python (= most notion users) 
  - [ ] build simple gui with tkinter (see: https://github.com/stars/sueszli/lists/python-guis) + executables for windows and osx
  - [ ] integrate into github actions such that people just need to enter their URL and immediately get a hosted version of the snapshot

- [ ] make contributing easier
  - [ ] build CI/CD end-to-end tests for PRs

- [ ] improve performance
  - [ ] concurrently download assets using https://docs.aiohttp.org/en/stable/client_quickstart.html#streaming-response-content

