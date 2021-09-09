# Copyright (C) 2020-2021 by CandyGang@Github, < https://github.com/CandyGang >.
#
# This file is part of < https://github.com/CandyGang/Cynics > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/CandyGang/Cynics/blob/master/LICENSE >
#
# All rights reserved.

import os
import asyncio
from datetime import datetime
from Cynics import PREFIX

from Cynics.setclient import CynicsCli
from pyrogram.types import Message
from pyrogram import filters

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""

`{PREFIX}ping`: Check Bot is Alive or Not.
"""

@CynicsCli.on_message(filters.command("ping", PREFIX) & filters.me)
async def pingme(_, message: Message):
    start = datetime.now()
    await message.edit("`Pong!`")
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await message.edit(f"**Pong!**\n`{m_s} ms`")
