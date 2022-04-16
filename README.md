# Lux-ray, A Discord Bot Write In Python
![Minimal Support Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue?style=flat-square)
[![Code style: black](https://img.shields.io/badge/code%20style-black-blue.svg?style=flat-square)](https://github.com/psf/black)
[![Commit activity](https://img.shields.io/github/commit-activity/w/euxcbsks/Lux-ray?style=flat-square)](https://github.com/Euxcbsks/Lux-ray/commits/main)
[![disnake latest](https://img.shields.io/badge/disnake-latest-blue?style=flat-square)](https://github.com/DisnakeDev/disnake)

- [Lux-ray, A Discord Bot Write In Python](#lux-ray-a-discord-bot-write-in-python)
- [Self-host](#self-host)
  - [If You Want Host Bot On Heroku](#if-you-want-host-bot-on-heroku)
  - [If You Want Host Bot On Replit](#if-you-want-host-bot-on-replit)
  - [Setup Database](#setup-database)
  - [Create A Bot Ttoken](#create-a-bot-ttoken)
  - [Edit bot-config.toml(optional)](#edit-bot-configtomloptional)
  - [Setup Environment Variable](#setup-environment-variable)
  - [Invite Your Bot](#invite-your-bot)
  - [Run Your Bot On Local Machine](#run-your-bot-on-local-machine)

# Self-host
## If You Want Host Bot On Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/Euxcbsks/Lux-ray)

## If You Want Host Bot On Replit
1. Import repo from github
2. Setup python env(need 5~10 min)
```Shell
> python setup_python3.8+.py
```

## Setup Database
*Current only support MongoDB*

You can use [MongoDB Atlas](https://www.mongodb.com/atlas/database) to get a free cloud db without cardit card.

Or you can [Install MongoDB](https://www.mongodb.com/docs/manual/installation/) on your local machine

If you choose to use atlas, follow the step below to create a free cluster
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas/database)
2. click `Try Free` at top.
3. Use Google account login or register below.
4. Create a new `Organization`
5. Create a new `Project` 
6. Create a new `Cluster` (You can create multiple project to get more free cluster)
7. Create a new `User` and follow the description
   * If you want connect to this project's cluster at anywhere, set IP filter to `0.0.0.0`
   * If you want only this machine can to connect this project's cluster, just click `Add My Current IP Address` button

## Create A Bot Ttoken
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click `New Applitcation` on top right and follow the step
3. Go to `Bot` page and click `Reset Token` to get token (***Token will not show again, so be sure to save it to somewhere***)

## Edit bot-config.toml(optional)
Modify the `bot-config.toml` to suit your needs

## Setup Environment Variable
If you host your bot on heroku, replit, or other services that can set environment variables, don't use the `.env` file.

This will cause Discord to reset the bot token and expose the database.

Or you can follow the step below
1. Rename `.env-sample` to `.env`
2. Modify `TOKEN_DEV` to you bot token
3. Modify `DB_HOST` to your database uri
   * If you use MongoDB Atlas provide database service, click `Connect` on the cluster page then click `Connect your application` to get the url (Don't select `Include full driver code example`)
   * If you install MongoDB on your local machine, uri will be `localhost:27017`

## Invite Your Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click the application you just create
3. Go to `OAuth` -> `URL Generator`
4. Select `bot` scope and permission you want to give your bot
5. Copy the url below and open it in a new page
6. Select a server you want use this bot and then follow the step

## Run Your Bot On Local Machine
1. Install bot requirements
```Shell
> python3 -m pip install -r "requirements.txt"
```
2. Launch MongoDB(if your `DB_HOST_DEV` is set to `localhost:271017`)
```Shell
> mongod
```
3. Launch bot
```Shell
> python3 lrb.py
```
