This is a collection of notes and considerations that were made during the development of the project.

<br><br>

## Downloading 

There are 3 ways to download the content of a Notion page:

1. Using the website's HTML feature
  This sucks - it is the very thing we are trying to avoid.
 
2. Using the official Notion.so API
  As done in [notion2html](https://github.com/MerkulovDaniil/notion4ever/tree/main/notion4ever): The user would need to generate a token / API key and it would be significantly more complicated to set up for each page. 

3. Scraping the HTML files directly from the browser
  This is the best option because the user does not have to do any extra work to get the app to work - but it is also the most complicated option.

<br><br>

## Choosing a scraping library

The following libraries were considered because they are the most popular and well supported (for Python as of March 2023):

- Playwright: https://playwright.dev/python/docs/intro
- Selenium: https://selenium-python.readthedocs.io/

Usually when installing a web driver you have to download the driver and add it to your `$PATH`. This is not ideal because it means that the user has to do extra work to get the app to work and you can not easily distribute the app as a single executable / dependency on a package manager.

Playwright has a built in driver manager which means that the user does not have to do any extra work to get the app to work. This is a big advantage over Selenium. But at the same time it has external dependencies that can not only installed with `pip` but also require the user to install other binaries.

This sucks because Playwright is also a lot more performant than Selenium.

But we managed to find a way to install Selenium with `pip` by using the `webdriver_manager` library. This means that we can use Selenium and the user does not have to do any extra work to get the app to work except having Python installed and running `pip`.

<br><br>

## Similar projects

There are already a few tools that do something very similar to what we want to do. We should try to build on top of these tools instead of reinventing the wheel.

I did a lot of research (really, I mean like 2 entire days) and found the following tools to have the best replication of the original styling:

- Loconotion: https://github.com/leoncvlt/loconotion/ (clearly the best option but it does not support all features - such as file attachments)
- Fruition: https://github.com/stephenou/fruitionsite/ (this one inspired Locotion)

<br>

We should just continue where Loconotion left off, because it is the best option.

We should make loconotion simpler and more opinionated by:
  - getting rid of the config `.toml` file and instead just offering a very minimal CLI interface
  - simplifying the installation process &rarr; ideally the user should be able to install the tool with a single command
