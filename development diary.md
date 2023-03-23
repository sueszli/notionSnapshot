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

## Choosing a strategy
There are 3 ways to fetch the content of a Notion.so page:

1. Exporting pages via the GUI tool and then optimizing the HTML files
  - Would result in some styling/information loss - the only changes would be through the use of CSS. Basically useless.
  
2. Using the official Notion.so API
  As done in [notion2html](https://github.com/MerkulovDaniil/notion4ever/tree/main/notion4ever).
  - Would result in some styling/information loss.
  - The user would need to generate a token / API key and it would be significantly more complicated to set up for each page. 
  - Kind of pointless, because it does not have any advantages over the default HTML export tool. <br>
  It would only be useful in combination to scraping, if some files are so large that the web driver crashes.

3. Scraping the HTML files directly from the browser
  - Would result in no styling/information loss at all.
  - Would be the most complicated to implement.

This means that the best option we really have is to scrape the HTML files directly from the browser although it feels like a very hacky solution.

<br><br>

## Choosing a language
JavaScript, Java, Python have the the best web-scraping libraries. Based on our experience, Java is too verbose.

We decided to use Python because it is the most popular language for data engineering and in general has the best data related eco-system. This means that there will be a larger community of developers to help with the project. It also means that there will be more resources available to help with the project and that the project will be easier to maintain.

<br><br>

## Choosing a scraping library
The following libraries were considered because they are the most popular and well supported:

- Playwright: https://playwright.dev/python/docs/intro
- Selenium: https://selenium-python.readthedocs.io/

Usually when installing a web driver you have to download the driver and add it to your `$PATH`. This is not ideal because it means that the user has to do extra work to get the app to work. Playwright has a built in driver manager which means that the user does not have to do any extra work to get the app to work. This is a big advantage over Selenium. But at the same time it has external dependencies that can not only installed with `pip` but also require the user to install extra software.

But we managed to find a way to install Selenium with `pip` by using the `webdriver_manager` library. This means that we can use Selenium and the user does not have to do any extra work to get the app to work except having Python installed and running `pip`.

<br><br>

## Finding existing tools to build on top of
There are already a few tools that do something very similar to what we want to do. We should try to build on top of these tools instead of reinventing the wheel.

I did a thorough research (really, I mean like 2 entire days) and found the following tools to have the best replication of the original styling:

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
