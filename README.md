```
    _   __      __  _                _____                        __          __
   / | / /___  / /_(_)___  ____     / ___/____  ____ _____  _____/ /_  ____  / /_
  /  |/ / __ \/ __/ / __ \/ __ \    \__ \/ __ \/ __ `/ __ \/ ___/ __ \/ __ \/ __/
 / /|  / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /_/ (__  ) / / / /_/ / /_
/_/ |_/\____/\__/_/\____/_/ /_/   /____/_/ /_/\__,_/ .___/____/_/ /_/\____/\__/
                                                    /_/

get pretty lookalikes of your pages through web-scraping
```

| <img width="685" src="docs/assets/export.jpeg"> | <img width="685" src="docs/assets/snapshot.jpeg"> | <img width="685" src="docs/assets/original.jpeg"> |
| :---------------------------------------------: | :-----------------------------------------------: | :-----------------------------------------------: |
|               Export with Notion                |        Scraped with **✨NotionSnapshot✨**        |                   Original page                   |

<br><br>

> [!IMPORTANT]  
> this project is unmaintained, for a reliable backup method check out: [NotionBackup](https://github.com/sueszli/notionBackup)
>
> pull requests are welcome. a docker script is provided for reproducability.

<br>

```bash
# install chrome (in wsl)
sudo apt update && sudo apt upgrade -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install
rm -rf google-chrome-stable_current_amd64.deb

# clone project
git clone https://github.com/sueszli/notionSnapshot/edit/master/README.md
cd notionSnapshot
pip install -r requirements.txt
python notionsnapshot --help

# example usage (see test.sh)
python notionsnapshot --dark-mode https://sueszli.notion.site/NotionSnapshot-Test-tiny-page-4dfa05657f774b45993542da4a8530c2
```

<br>

many thanks to:

-   [@leoncvlt](https://github.com/leoncvlt) who laid the foundation of this project through loconotion (this project is a complete rewrite)
-   [@mjdeligan](https://github.com/MJDeligan) who heavily optimized the performance and implemented the caching and recursive crawling functionality
-   [@stefnotch](https://github.com/stefnotch/) and [@thomasbiede](https://github.com/ThomasBiede) who helped me set the project up
