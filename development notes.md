# Development Notes
This is a collection of notes and considerations for the development of the project.

<br>

## Defining the problem
The default HTML export tool in Notion.so does not keep the pages original styling and formatting. Providing an alternative HTML export tool that keeps the pages original styling and formatting would also enable people to...

- ... use Notion.so as a CMS for their website (so they no longer need super.so, potion.so, etc.) - additionally the pages could also be immediately hosted on GitHub-Pages.
- ... leave the Notion.so ecosystem by backing up their data.

We initially wanted to build a GUI such that non-technical users could use the tool. But we decided to build a CLI tool instead because it is easier to build and maintain. We also decided to build a CLI tool because it is easier to integrate with other tools, that is, it is easier to build a GUI on top of a CLI tool than the other way around.

In short: This should be a simple CLI tool that converts Notion.so pages to HTML files (for developers).

<br>

## Choosing a language
JavaScript, Java, Python have the the best web-scraping libraries. Based on our experience, JavaScript and Python were easier to write scripting tools.

We decided to use Python because it is the most popular language for data engineering and in general has the best data related eco-system. This means that there will be a larger community of developers to help with the project. It also means that there will be more resources available to help with the project and that the project will be easier to maintain.

<br>

## Choosing a scraping library
The following libraries were considered because they are the most popular and well supported:

- Playwright: https://playwright.dev/python/docs/intro
- Selenium: https://selenium-python.readthedocs.io/

Usually when installing a web driver you have to download the driver and add it to your `$PATH`. This is not ideal because it means that the user has to do extra work to get the app to work. Playwright has a built in driver manager which means that the user does not have to do any extra work to get the app to work. This is a big advantage over Selenium. But at the same time it has external dependencies that can not only installed with `pip` but also require the user to install extra software.

But we managed to find a way to install Selenium with `pip` by using the `webdriver_manager` library. This means that we can use Selenium and the user does not have to do any extra work to get the app to work except having Python installed and running `pip`.

<br>

## Building on top of existing tools
There are already a few tools that do something very similar to what we want to do. We should try to build on top of these tools instead of reinventing the wheel.

- Loconotion: https://github.com/leoncvlt/loconotion/
- Fruition: https://github.com/stephenou/fruitionsite/

I've tried all available tools that I could find and I've found that Loconotion mimics the original styling the best. But it is not actively maintained and it does not support all features (e.g. file attachments).

Here are the things that I think we should do differently:

- improving overall code quality
  - writing all modules into a single file
- improving installation and usage process
  - getting rid of Docker by using the `webdriver_manager` library
  - getting rid of the config `.toml` file and instead just offering a very minimal CLI interface (e.g. opinionated defaults that can't be changed)
- accessing the Notion.so API directly instead of using web scraping. this would make the tool more robust and faster, and it would also make it easier to support all features

<br>