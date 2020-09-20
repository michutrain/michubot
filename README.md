# michu bot

<img src="https://cdn.discordapp.com/attachments/755958167908909108/756009280234324078/Untitled-1.png"  width="200" height="auto">

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [planned 🚧](#planned)

## General info
wip all purpose bot!

currently hosting a self managed win/loss leaderboard, titled for inhouse valorant rankings. 

can be configured to use both a PostgreSQL database or writing to a local json file instead

## Setup
download python at https://www.python.org/downloads/

#### Packages
psycopg2 is only if you're using a PostgreSQL database, skip if you are writing to json
```
$ pip install dotenv
$ pip install discord.py
*********************
$ pip install psycopg2
```
environmental variables are configured in the .env file,  replace everything after the =, even the <> brackets
```
DISCORD_TOKEN = found on the https://discord.com/developers/applications portal for your bot
DISCORD_GUILD = <not currently in use>
DB_HOST = your postgresql server, localhost if it's self hosted
PORT = default is 5432
DB_USER = default is postgres
DB_PASSWORD = set when configuring db
DB_NAME = set when configuring db
```

#### Running the Bot
place the bot.py script in a directory as the leaderboard is written in a file. run with:
```
py bot.py
```
## planned 🚧
- ~~sorting by win~~
- ~~map randomizer~~
- ~~win loss ratio~~
- ~~elo ladder based on scaled win loss~~
- matchmaking randomizer based on who's signed up
- more bot features!!!
stay tuned!
