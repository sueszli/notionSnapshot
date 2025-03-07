```
    _   __      __  _                _____                        __          __
   / | / /___  / /_(_)___  ____     / ___/____  ____ _____  _____/ /_  ____  / /_
  /  |/ / __ \/ __/ / __ \/ __ \    \__ \/ __ \/ __ `/ __ \/ ___/ __ \/ __ \/ __/
 / /|  / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /_/ (__  ) / / / /_/ / /_
/_/ |_/\____/\__/_/\____/_/ /_/   /____/_/ /_/\__,_/ .___/____/_/ /_/\____/\__/
                                                  /_/
```

| <img width="685" src="docs/assets/export.jpeg"> | <img width="685" src="docs/assets/snapshot.jpeg"> | <img width="685" src="docs/assets/original.jpeg"> |
| :---------------------------------------------: | :-----------------------------------------------: | :-----------------------------------------------: |
|               Export with Notion                |        Scraped with **✨NotionSnapshot✨**        |                   Original page                   |

# usage

> [!IMPORTANT]  
> this project is unmaintained, but functional. but pull requests are welcome. a docker script is provided for reproducibility.
>
> for a more reliable backup strategy check out: [NotionBackup](https://github.com/sueszli/notionBackup)

```bash
# install chrome (in case you're using windows subsystem for linux)
sudo apt update && sudo apt upgrade -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install
rm -rf google-chrome-stable_current_amd64.deb

# clone project
git clone https://github.com/sueszli/notionSnapshot
cd notionSnapshot
pip install -r requirements.txt

# demo
python notionsnapshot --help
python notionsnapshot --dark-mode https://sueszli.notion.site/NotionSnapshot-Test-tiny-page-4dfa05657f774b45993542da4a8530c2
```
# kudos

many thanks to:

-   [@leoncvlt](https://github.com/leoncvlt) who laid the foundation of this project through loconotion (this project is a complete rewrite)
-   [@mjdeligan](https://github.com/MJDeligan) who heavily optimized the performance and implemented the caching and recursive crawling functionality
-   [@stefnotch](https://github.com/stefnotch/) and [@thomasbiede](https://github.com/ThomasBiede) who helped me set the project up
