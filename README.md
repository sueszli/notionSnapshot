```
    _   __      __  _                _____                        __          __
   / | / /___  / /_(_)___  ____     / ___/____  ____ _____  _____/ /_  ____  / /_
  /  |/ / __ \/ __/ / __ \/ __ \    \__ \/ __ \/ __ `/ __ \/ ___/ __ \/ __ \/ __/
 / /|  / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /_/ (__  ) / / / /_/ / /_
/_/ |_/\____/\__/_/\____/_/ /_/   /____/_/ /_/\__,_/ .___/____/_/ /_/\____/\__/
                                                    /_/

A web scraper for Notion.
Get pretty offline duplicates of your pages: No extra JavaScript, no extra bulk, no extra wait!
```

| <img width="685" src="docs/assets/export.jpeg"> | <img width="685" src="docs/assets/snapshot.jpeg"> | <img width="685" src="docs/assets/original.jpeg"> |
| :---------------------------------------------: | :-----------------------------------------------: | :-----------------------------------------------: |
|               Export with Notion                |        Scraped with **✨NotionSnapshot✨**         |                   Original page                   |

<br>

> _Before using, keep in mind:_ Webscraping is not safe backup method. \
> This project aims to generate look-alike copies of your Notion pages – not to back your data up. 
> For a more reliable option, check out '[NotionBackup](https://github.com/sueszli/notionBackup)' which fixes Notion's standard HTML exports.

<br><br><br><br>

# How to use

<br>

1. Share Notion page on the web

    To be able to scrape a Notion page, it has to be publicly accessible.
    
    On your Notion page, navigate to the `Publish` tab and publish your page to the web.

<br>

2. Install Python and Chrome

    Next, ensure that you have the necessary apps installed on your machine:

    -   [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install) if you're running Windows, as this tool is designed for MacOS / Linux

    -   [Python 3](https://www.python.org/downloads/)

    -   [Chrome](https://www.google.com/chrome/)

        <details>
        <summary>Installing chrome on WSL2/Ubuntu can be a bit difficult</summary>

        Installing headless Chrome on a Debian system may require a few extra steps:

        ```bash
        # install chrome on wsl/ubuntu
        sudo apt update && sudo apt upgrade -y
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo dpkg -i google-chrome-stable_current_amd64.deb
        sudo apt --fix-broken install
        rm -rf google-chrome-stable_current_amd64.deb
        ```
        </details>

<br>

3. Run script

    Then just run the following bash script:

    ```bash
    # clone
    git clone https://github.com/sueszli/notionSnapshot.git
    cd notionSnapshot

    # install dependencies
    if command -v python3 &>/dev/null; then echo "Python 3 is installed."; else echo "Python 3 is not installed."; fi
    python3 -m pip install --upgrade pip > /dev/null
    pip3 install pipreqs > /dev/null && rm -rf requirements.txt > /dev/null && pipreqs . > /dev/null
    pip3 install -r requirements.txt > /dev/null

    # run
    python3 notionsnapshot --help

    # example usage
    python3 notionsnapshot --dark-mode https://sueszli.notion.site/NotionSnapshot-Test-tiny-page-4dfa05657f774b45993542da4a8530c2
    ```

<br><br><br><br>

---

<br>

<span style="color:grey;">

Special thanks to:

-   Leonardo Cavaletti who laid the foundation of this project through Loconotion (this project is a complete rewrite)
-   Marco / MJDeligan who heavily optimized the performance and implemented the caching and recursive crawling functionality
-   Stefan Brandmair, Thomas Biedermann and Berndt Uhlig who helped me set the project up

</span>
