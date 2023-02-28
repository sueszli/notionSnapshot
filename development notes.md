# Development Notes
This is a collection of notes and considerations for the development of the project.

<br>

## Defining the problem
The default HTML export tool in Notion.so does not keep the pages original styling and formatting. Providing an alternative HTML export tool that keeps the pages original styling and formatting would also enable people to:

- Use Notion.so as a CMS for their website (so they no longer need super.so, potion.so, etc.) - additionally the pages could also be immediately hosted though GitHub Pages
- Leave the Notion.so ecosystem by backing up their data to static websites with identical styling

<br>

## Choosing a language
JavaScript, Java, Python have the the best web-scraping libraries. JavaScript is better at handling asynchronous requests which could significantly improve the apps performance. However, Python also has `asyncio` which could be used to achieve the same result.

We decided to use Python because it is the most popular language for data engineering and in general has the best data related eco-system. This means that there will be a larger community of developers to help with the project. It also means that there will be more resources available to help with the project and that the project will be easier to maintain.

<br>

## Choosing a scraping library
The following libraries were considered because they are the most popular and well supported:

- Playwright: https://playwright.dev/python/docs/intro
- Selenium: https://selenium-python.readthedocs.io/

Usually when installing a web driver you have to download the driver and add it to your `$PATH`. This is not ideal because it means that the user has to do extra work to get the app to work. Playwright has a built in driver manager which means that the user does not have to do any extra work to get the app to work. This is a big advantage over Selenium. But at the same time it has external dependencies that can not only installed with `pip` but also require the user to install extra software.

But we managed to find a way to install Selenium with `pip` by using the `webdriver_manager` library. This means that we can use Selenium and the user does not have to do any extra work to get the app to work except having Python installed and running `pip`.

<br>

