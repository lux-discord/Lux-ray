# Lux-ray, a Discord bot write in python
![Minimal Support Python Version](https://img.shields.io/badge/python-3.9-blue?style=flat-square)

# Self-host
## If you want host bot on replit
1. Import repo from github
2. Setup python env(need 5~10 min)
> python setup_python3.8+.py

## Database setup
*Current only support MongoDB*

You can use [MongoDB Atlas](https://www.mongodb.com/atlas/database) to get a free cloud db without cardit card.

### Create a free cluster (if use atlas)
1. click `Try Free` at top.
2. Use Google account login or register below.
3. Create a new `Organization`
4. Create a new `Project` 
5. Create a new `Cluster` (You can create multiple project to get more free cluster)
6. Create a new `User` and follow the description
   * If you want connect to this project's cluster at anywhere, set IP filter to `0.0.0.0`
   * If you want only this machine can to connect this project's cluster, just click `Add My Current IP Address` button

## Create a bot token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click `New Applitcation` on top right and follow the step
3. Go to `Bot` page and click `Reset Token` to get token
   * **Token will not show again, so be sure to save it at somewhere**

## Edit bot-config.toml
1. Rename `sample-bot-config.toml` to `bot-config.toml`
2. Modify `database.dev.url` to your database url
   * You can click `Connect` on the cluster page and then click `Connect your application` to get the url(Don't select `Include full driver code example`)
3. Modify `token.dev` or `token.all` to your bot token

## Invite your bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click the application you just create
3. Go to `OAuth` -> `URL Generator`
4. Select `bot` scope and permission you want to give your bot
5. Copy the url below and open it in a new page
6. Select a server you want use this bot and then follow the step

## Run
1. Install requirement
> python3 -m pip install -r "requirements-common.txt"
2. run
> python3 lrb.py
