from __future__ import annotations

import asyncio
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

from config import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


class ManagementBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
        )

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.management")

        guild_id = settings.command_sync_guild_id
        if guild_id:
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logging.info("Synced %s commands to guild %s", len(synced), guild_id)
        else:
            synced = await self.tree.sync()
            logging.info("Synced %s global commands", len(synced))

    async def on_ready(self) -> None:
        if self.user:
            logging.info("Logged in as %s (%s)", self.user, self.user.id)


async def main() -> None:
    token = settings.discord_token
    if not token:
        raise RuntimeError("DISCORD_TOKEN is not set.")

    bot = ManagementBot()
    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
