# Copyright (C) 2020-2021 by CandyGang@Github, < https://github.com/CandyGang >.
#
# This file is part of < https://github.com/CandyGang/Cynics > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/CandyGang/Cynics/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from Cynics.plugins import ALL_PLUGINS
from Cynics import APP_ID, API_HASH, STRING_SESSION, LOGGER, load_cmds, name

from Cynics import PREFIX


class CynicsCli(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            STRING_SESSION,
            plugins=dict(root=f"Cynics/plugins"),
            workdir=f"{name}/session",
            api_id=APP_ID,
            api_hash=API_HASH,
        )

    async def start(self):
        await super().start()
        result = load_cmds(ALL_PLUGINS)
        LOGGER.info(result)

        me = await self.get_me()
        LOGGER.info(
            f"Cynics Userbot based on Pyrogram v{__version__} "
            f"(Layer {layer}) started...\n"
            f"Hey {me.first_name}! Userbot Started Type {PREFIX}help in Any Telegram Chat."
        )

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("Your Userbot stopped. Bye.")
