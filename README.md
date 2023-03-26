```
    _   __      __  _                _____                        __          __ 
   / | / /___  / /_(_)___  ____     / ___/____  ____ _____  _____/ /_  ____  / /_
  /  |/ / __ \/ __/ / __ \/ __ \    \__ \/ __ \/ __ `/ __ \/ ___/ __ \/ __ \/ __/
 / /|  / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /_/ (__  ) / / / /_/ / /_  
/_/ |_/\____/\__/_/\____/_/ /_/   /____/_/ /_/\__,_/ .___/____/_/ /_/\____/\__/  
                                                    /_/     

📸💥 the html export tool that actually works

- free yourself from the Notion lock-in
- use Notion as your content management system
- share your Notion pages with custom domain names
```

<br>

Original page              |  Export through Notion | **✨Notion Snapshot✨**
:-------------------------:|:-------------------------:|:-------------------------:
<img width="685" alt="image" src="https://user-images.githubusercontent.com/61852663/221595552-3eebc492-9e64-4cb3-b330-4418961890ce.png">  |  <img width="685" alt="image" src="https://user-images.githubusercontent.com/61852663/221595560-d90a2d41-f7a8-48be-8fe9-e63889126042.png">               | <img width="685" alt="image" src="https://user-images.githubusercontent.com/61852663/221595539-ba0b9dca-4bd4-482e-81f9-64ea12e0ded4.png">

<br><br><br>

# How to use

### 1. Make your Notion page publicly accessible
Assuming that you already have a [www.notion.so](https://www.notion.so/) account, you can make your pages publicly accessible by clicking on the `Share` button in the top right corner of the page and toggling the `Share to web` button.

You then need to `Copy web link` for the next steps.

<br>

### 2a. Download the executalbe

```bash
git clone https://github.com/sueszli/notionSnapshot.git
cd notionSnapshot
``` 

</br>

### 2b. Clone this repository
```bash
git clone https://github.com/sueszli/notionSnapshot.git
cd notionSnapshot
``` 

</br>

### 3. Install dependencies
This Python project uses [Poetry](https://python-poetry.org/) for dependency management. To install the dependencies install Poetry and then run:

```
poetry install --sync
```

Note: If running Poetry isn't enough, you need to install the missing dependencies manually with `pip` / `pip3` (I still have to find a fix for this).

</br>

### 4. Run
Use the `-h` or `--help` flag to see all the available options.

Replace the URL with the one you generated in the first step.
After runnning the script the exported files will be saved in the `snapshots` folder.

_Unix:_
```bash
# if you are running Ubuntu in WSL, you must additionally install Chrome like so
sudo apt update && sudo apt upgrade -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install
rm -rf google-chrome-stable_current_amd64.deb

python3 notionsnapshot https://eager-waterfall-308.notion.site/Loconotion-Example-03c403f4fdc94cc1b315b9469a8950ef
```

_Windows:_
```bash
py notionsnapshot https://eager-waterfall-308.notion.site/Loconotion-Example-03c403f4fdc94cc1b315b9469a8950ef
```

<br><br><br>

# Testing
For now, we are trying to refactor Loconotion before improving upon it and adding new features:
- Input URL: https://eager-waterfall-308.notion.site/Loconotion-Example-03c403f4fdc94cc1b315b9469a8950ef
- Expected output: https://loconotion-example.netlify.app/

<br><br><br>

# Thank you
I hope you enjoy using this project as much as we enjoyed making it.
There are a lot of people to thank for this project, so here's a list of everyone who deserves a big thank you:

- [Leonardo Cavaletti](mailto:impeto.blu@gmail.com) and his team for their fantastic work on the [Loconotion](https://github.com/leoncvlt/loconotion) project, which provided the foundation for this one.
- All the wonderful individual contributors
- All the users that reported bugs, and made feature requests, helping to make this project a success
