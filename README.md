```
    _   __      __  _                _____                        __          __ 
   / | / /___  / /_(_)___  ____     / ___/____  ____ _____  _____/ /_  ____  / /_
  /  |/ / __ \/ __/ / __ \/ __ \    \__ \/ __ \/ __ `/ __ \/ ___/ __ \/ __ \/ __/
 / /|  / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /_/ (__  ) / / / /_/ / /_  
/_/ |_/\____/\__/_/\____/_/ /_/   /____/_/ /_/\__,_/ .___/____/_/ /_/\____/\__/  
                                                    /_/     
                                                    
       --- Export your Notion pages as HTML files, that look great! ---

```

<br>

Original page              |  Export through Notion | **✨NotionSnapshot✨**
:-------------------------:|:-------------------------:|:-------------------------:
<img width="685" alt="image" src="https://user-images.githubusercontent.com/61852663/221595552-3eebc492-9e64-4cb3-b330-4418961890ce.png">  |  <img width="685" alt="image" src="https://user-images.githubusercontent.com/61852663/221595560-d90a2d41-f7a8-48be-8fe9-e63889126042.png">               | <img width="685" alt="image" src="https://user-images.githubusercontent.com/61852663/221595539-ba0b9dca-4bd4-482e-81f9-64ea12e0ded4.png">

^ the ducks are just placeholders for the images lol (this project is still a work in progress)

<br><br><br>

### 1. Make a publically accessible page
Assuming you already have a [www.notion.so](https://www.notion.so/) account, you can make your pages publicly accessible by clicking on the `Share` button in the top right corner of the page and toggling the `Share to web` button.

You will need the generated link for the next step.

<br>

### 2. Clone this repository
```bash
git clone https://github.com/sueszli/notionSnapshot.git
cd notionSnapshot
``` 

</br>

### 3. Install dependencies
This Python project uses [Poetry](https://python-poetry.org/) for dependency management. To install the dependencies install Poetry and then run:

```bash
poetry install --sync
```

Note: If running Poetry isn't enough, you need to install the missing dependencies manually with `pip` / `pip3` (I still have to find a fix for this).

</br>

### 4. Run
Use the `-h` or `--help` flag to see all possible arguments.

Replace the URL with the one you generated in the first step.

_Unix:_
```bash
# if you are running Ubuntu in WSL, you must additionally install Chrome like so
sudo apt update && sudo apt upgrade -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install
rm -rf google-chrome-stable_current_amd64.deb

python3 notionsnapshot https://www.notion.so/Loconotion-Example-03c403f4fdc94cc1b315b9469a8950ef
```

_Windows:_
```powershell
py notionsnapshot https://www.notion.so/Loconotion-Example-03c403f4fdc94cc1b315b9469a8950ef
```

<br>

### 5. Enjoy
The exported HTML file will be saved in the `snapshots` folder.

A big thank you to:

- Leonardo Cavaletti and his team for their fantastic work on the (Loconotion)[https://github.com/leoncvlt] project, which provided the foundation for this project.
- All the wonderful individuals who have contributed, reported bugs, and made feature requests, helping to make this project a success.
