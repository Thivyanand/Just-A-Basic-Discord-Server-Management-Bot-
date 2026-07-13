# Just-A-Basic-Discord-Server-Management-Bot-

A small Python Discord bot built with `discord.py` for server moderation and management. It uses slash commands, is ready for GitHub, and includes the basic project files you need to start and deploy it cleanly.

## Features

- Slash commands for moderation and server management
- `ping`, `serverinfo`, and `userinfo`
- `purge`, `kick`, `ban`, `unban`, `timeout`, and `untimeout`
- `slowmode`, `lock`, and `unlock`
- `.env`-based configuration
- GitHub Actions workflow for basic validation

## Requirements

- Python 3.10+ recommended
- A Discord application and bot token
- Privileged intents enabled in the Discord Developer Portal for member actions

## Setup

1. Create and activate the virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and fill in your bot token.
4. Run the bot with `python bot.py`.

## Environment Variables

- `DISCORD_TOKEN`: your bot token
- `DISCORD_GUILD_ID`: optional guild ID for testing slash command sync locally
- `COMMAND_SYNC_GUILD_ID`: optional alias for `DISCORD_GUILD_ID`

## Running Locally

```bash
python -m pip install -r requirements.txt
python bot.py
```

If you set `DISCORD_GUILD_ID` or `COMMAND_SYNC_GUILD_ID`, slash commands sync to that server immediately. Otherwise they sync globally.

## Invite URL

Use the Discord Developer Portal to generate an invite URL with at least these scopes and permissions:

- `bot`
- `applications.commands`
- `Kick Members`
- `Ban Members`
- `Moderate Members`
- `Manage Channels`
- `Manage Messages`

## GitHub Ready

This repository already includes:

- `.gitignore`
- `.env.example`
- `requirements.txt`
- `README.md`
- GitHub Actions workflow

After you add your remote, commit the files and push as usual.
