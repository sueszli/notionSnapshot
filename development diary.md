This is a collection of notes and considerations that were made during the development of the project.

<br><br>

## Defining the problem
The default HTML export tool in Notion.so does not keep the pages original styling and formatting. Providing an alternative HTML export tool that keeps the pages original styling and formatting would also enable people to ...

- leave the Notion.so ecosystem by backing up their data.
- use Notion.so as a CMS for their website (so they no longer need super.so, potion.so, etc.) - additionally the pages could also be immediately hosted on GitHub-Pages.

We initially wanted to build a GUI such that non-technical users could use the tool. We decided to build a CLI tool instead because ...
- it is easier to build and maintain
- it is easier to integrate with other tools, that is, it is easier to build a GUI on top of a CLI tool than the other way around.

Ideally the tool should be a standalone library that can be used by other developers to build their own tools.

In short: This should be a simple CLI tool that converts Notion.so pages to HTML files (for developers).

<br><br>

## Choosing a language
JavaScript, Java, Python have the the best web-scraping libraries. Based on our experience, JavaScript and  were easier to write scripting tools.

We decided to use Python because it is the most popular language for data engineering and in general has the best data related eco-system. This means that there will be a larger community of developers to help with the project. It also means that there will be more resources available to help with the project and that the project will be easier to maintain.

<br><br>

## Choosing a strategy
There are 3 ways to fetch the content of a Notion.so page:

1. Exporting pages via the GUI tool and then optimizing the HTML files
  - Would result in some styling/information loss - the only changes would be through the use of CSS. Basically useless.
  
2. Using the official Notion.so API
  As done in [notion2html](https://github.com/MerkulovDaniil/notion4ever/tree/main/notion4ever).
  - Would result in some styling/information loss.
  - Kind of pointless, because it does not have any advantages over the default HTML export tool.
  - The user would need to generate a token / API key and it would be significantly more complicated to set up for each page.

3. Scraping the HTML files directly from the browser
  - Would result in no styling/information loss at all.
  - Would be the most complicated to implement.

The third option is the most complicated to implement but it is also the most powerful. It is also the only option that would result in no styling/information loss (which is why we started in the first place). This is why we decided to go with this option.

If files are too large to be scraped, we can use the official Notion.so API to retrieve the data and then use the HTML scraping tool to retrieve the styling - but this is not a priority and would only be necessary for very large pages.

<br><br>

## Choosing a scraping library
The following libraries were considered because they are the most popular and well supported:

- Playwright: https://playwright.dev/python/docs/intro
- Selenium: https://selenium-python.readthedocs.io/

Usually when installing a web driver you have to download the driver and add it to your `$PATH`. This is not ideal because it means that the user has to do extra work to get the app to work. Playwright has a built in driver manager which means that the user does not have to do any extra work to get the app to work. This is a big advantage over Selenium. But at the same time it has external dependencies that can not only installed with `pip` but also require the user to install extra software.

But we managed to find a way to install Selenium with `pip` by using the `webdriver_manager` library. This means that we can use Selenium and the user does not have to do any extra work to get the app to work except having Python installed and running `pip`.

<br><br>

## Finding the best scraping tool
There are already a few tools that do something very similar to what we want to do. We should try to build on top of these tools instead of reinventing the wheel.

I did a thorough research (really, I mean like 2 full days) and found the following tools to have the best replication of the original styling:

- Loconotion: https://github.com/leoncvlt/loconotion/ (clearly the best option but it does not support all features - such as file attachments)
- Fruition: https://github.com/stephenou/fruitionsite/ (this one inspired Locotion)

<br>

In short: We should just continue where Loconotion left off, because it is the best option.

The is how we can improve on it:

- _making the tool simpler and more opinionated:_
  - getting rid of the config `.toml` file and instead just offering a very minimal CLI interface
  - simplifying the installation process &rarr; ideally the user should be able to install the tool with a single command (i.e. `brew install notionsnapshot`)

- _making the tool more powerful and reliable:_
  - supporting more blocks (i.e. file attachments, more types of embeds, etc.)
  - using the official Notion.so API to retrieve some of the data (see below)
