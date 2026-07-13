# Basic Discord Management Bot

A small Python Discord bot built with `discord.py` for server management, uses / commands s

## Features

- Slash commands
- `ping`,
- `purge`, `kick`, `ban`, `unban`, `timeout`, and `untimeout`
- `slowmode`, `lock`, and `unlock`
- `.env`-based configuration


## Requirements

- Python 3.10+ recommended
- A Discord application and bot token
- Bot must have perms

## Setup

1. Create and activate the env
2. Install dependencies with pip install -r requirements.txt
3. Copy `.env.example` to .env and fill in your bot token.
4. Run the bot with python bot.py

## ENV

- `DISCORD_TOKEN`: your bot token
- `DISCORD_GUILD_ID`: optional guild ID for testing slash command sync locally
- `COMMAND_SYNC_GUILD_ID`: optional alias for `DISCORD_GUILD_ID`

## Running Locally

python -m pip install -r requirements.txt
python bot.py

## Invite URL

Use the Discord Developer Portal to generate an oAuth URL with at least these perms:

- `bot`
- `applications.commands`
- `Kick Members`
- `Ban Members`
- `Moderate Members`
- `Manage Channels`
- `Manage Messages`

Thank you for using , this template 
