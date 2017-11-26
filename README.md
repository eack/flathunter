# Python Flathunter-Helper

## Info
This is a fork from [flathunter](https://github.com/NodyHub/flathunter). flathunter is a brilliant tool, that scans flatportals and sends notifications via Telegram when new exposes arrive.

## Supported platforms
- [ImmobilienScout24](https://www.immobilienscout24.de)
- [WG-gesucht](http://www.wg-gesucht.de)
- [ebay-kleinanzeigen](https://www.ebay-kleinanzeigen.de)
- [immonet](https://www.immonet.de)
- [immowelt](https://www.immowelt.de/)

## Setup

### Virtual Environment (Optional)
To keep you python environment and site-packages clean, it is recommended
to run the project in a virtual environment. Install ```virtualenv```,
create a venv and activate.
```
$ pip install virtualenv
$ virtualenv -p /usr/bin/python3.6 venv
$ source venv/bin/activate
```


### Requirements
Install requirements from ```requirements.txt``` to run execute flathunter properly.
```
pip install -r requirements.txt
```

## Usage
```
usage: flathunter.py [-h] [--config CONFIG]

Searches for flats on Immobilienscout24.de and wg-gesucht.de and sends results
to Telegram User

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Config file to use. If not set, try to use
                        '~git-clone-dir/config.yaml'

```

### Configuration

#### Bot registration
A new bot can registered with the telegram chat with the [BotFather](https://telegram.me/BotFather).

#### Chat-Ids
To get the chat id, the [REST-Api](https://core.telegram.org/bots/api) of telegram can be used to fetch the received messages of the Bot.
```
$ curl https://api.telegram.org/bot[BOT-TOKEN]/getUpdates
```

#### Google API
To use the distance calculation feature a [Google API-Key](https://developers.google.com/maps/documentation/javascript/get-api-key) is needed.

## Todos

- [ ] Add better error handling to crawlers
- [ ] Add option in config to hide preview image

If you need a new feature feel free to create a new issue.

## Contributers
- [@NodyHub](https://github.com/NodyHub)
- Bene
- [@Cugu](https://github.com/Cugu)
- [@eack](https://github.com/eack)


