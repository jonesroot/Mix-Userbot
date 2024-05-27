import asyncio
import sys
from pyrogram import idle
from pyrogram.errors import *

from beban import (autor_all, autor_bot, autor_ch, autor_gc, autor_mention,
                   autor_us)
from Mix import *
from Mix.core.gclog import check_logger, getFinish
from Mix.core.waktu import auto_clean

loop = asyncio.get_event_loop_policy()
event_loop = loop.get_event_loop()


async def start_user():
    LOGGER.info(f"Starting Telegram User Client...")
    try:
        await nlx.start()
    except (SessionExpired, ApiIdInvalid, UserDeactivatedBan):
        LOGGER.info("Check your session or api id!!")
        sys.exit(1)


async def start_bot():
    LOGGER.info(f"Starting Telegram Bot Client...")
    if TOKEN_BOT is None:
        await autobot()
    try:
        await bot.start()
    except SessionRevoked as e:
        print(f"Error : {e}")
        LOGGER.info("Token Expired.")
        ndB.del_key("BOT_TOKEN")
        sys.exit(1)
    except AccessTokenInvalid as e:
        print(f"Error : {e}")
        ndB.del_key("BOT_TOKEN")
        sys.exit(1)
    except AccessTokenExpired:
        print("Error : {e}")
        ndB.del_key("BOT_TOKEN")
        sys.exit(1)


async def starter():
    LOGGER.info(f"Check Updater...")
    await cek_updater()
    LOGGER.info(f"Updater Finished...")
    LOGGER.info(f"Connecting to {ndB.name}...")
    if ndB.ping():
        LOGGER.info(f"Connected to {ndB.name} Successfully!")
    await start_user()
    if nlx.is_connected:
        await start_bot()
        await check_logger()


async def main():
    await starter()
    await asyncio.gather(refresh_cache(), getFinish())
    LOGGER.info("Successfully Started Userbot.")
    task_afk = asyncio.create_task(auto_clean())
    task_gc = asyncio.create_task(autor_gc())
    task_ch = asyncio.create_task(autor_ch())
    task_us = asyncio.create_task(autor_us())
    task_bot = asyncio.create_task(autor_bot())
    task_tag = asyncio.create_task(autor_mention())
    task_all = asyncio.create_task(autor_all())
    await asyncio.gather(
        task_afk,
        task_tag,
        task_gc,
        task_ch,
        task_us,
        task_bot,
        task_all,
        isFinish(),
        idle(),
    )


if __name__ == "__main__":
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())
