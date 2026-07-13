from __future__ import annotations

from dataclasses import dataclass
import os


def _read_int(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


@dataclass(frozen=True)
class Settings:
    discord_token: str | None
    command_sync_guild_id: int | None


settings = Settings(
    discord_token=os.getenv("DISCORD_TOKEN"),
    command_sync_guild_id=_read_int(os.getenv("COMMAND_SYNC_GUILD_ID") or os.getenv("DISCORD_GUILD_ID")),
)
