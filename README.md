```
    _   __      __  _                _____                        __          __
   / | / /___  / /_(_)___  ____     / ___/____  ____ _____  _____/ /_  ____  / /_
  /  |/ / __ \/ __/ / __ \/ __ \    \__ \/ __ \/ __ `/ __ \/ ___/ __ \/ __ \/ __/
 / /|  / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /_/ (__  ) / / / /_/ / /_
/_/ |_/\____/\__/_/\____/_/ /_/   /____/_/ /_/\__,_/ .___/____/_/ /_/\____/\__/
                                                    /_/

Get pretty lookalike duplicates of your pages by web-scraping.
```

<br>

| <img width="685" src="docs/assets/export.jpeg"> | <img width="685" src="docs/assets/snapshot.jpeg"> | <img width="685" src="docs/assets/original.jpeg"> |
| :---------------------------------------------: | :-----------------------------------------------: | :-----------------------------------------------: |
|               Export with Notion                |        Scraped with **✨NotionSnapshot✨**        |                   Original page                   |

<br>

> [!WARNING]
> Project not actively maintained, but pull-requests are welcome.
>
> Also: this is not a safe backup method. Check out [NotionBackup](https://github.com/sueszli/notionBackup) to fix Notion's standard HTML exports.

<br><br><br>

# How to use

1. Make your Notion pages publicly accessible

    On your Notion page, navigate to the `Publish` tab and publish your page to the web.

2. Install Google Chrome (in addition to python)

    Download google chrome here: https://www.google.com/chrome/

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

3. Run script

    Use Linux, MacOS or WSL (on Windows).

    ```bash
    # install dependencies
    pip install pipreqs
    rm -rf requirements.txt && pipreqs .
    pip install -r requirements.txt

    # run
    python3 notionsnapshot --help

    # example usage
    python3 notionsnapshot --dark-mode https://sueszli.notion.site/NotionSnapshot-Test-tiny-page-4dfa05657f774b45993542da4a8530c2
    ```

<br><br><br>

> Special thanks to:
>
> -   [@leoncvlt](https://github.com/leoncvlt) who laid the foundation of this project through Loconotion (this project is a complete rewrite)
> -   [@mjdeligan](https://github.com/MJDeligan) who heavily optimized the performance and implemented the caching and recursive crawling functionality
> -   [@stefnotch](https://github.com/stefnotch/) and [@thomasbiede](https://github.com/ThomasBiede) who helped me set the project up
