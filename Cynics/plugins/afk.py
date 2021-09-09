# Copyright (C) 2020-2021 by CandyGang@Github, < https://github.com/CandyGang >.
#
# This file is part of < https://github.com/CandyGang/Cynics > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/CandyGang/Cynics/blob/master/LICENSE >
#
# All rights reserved.

import time
from pyrogram import filters
import asyncio

from pyrogram.types import Message

from Cynics import PREFIX, PRIVATE_GROUP_ID
from Cynics.setclient import CynicsCli
from Cynics.helpers.pyrohelper import get_arg
import Cynics.db.afkdb as Cynics
from Cynics.helpers.pyrohelper import user_afk
from Cynics.helpers.pyrohelper import get_readable_time
from Cynics.helpers.utils.utils import get_message_type, Types


LOG_GROUP = PRIVATE_GROUP_ID

MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 60


@CynicsCli.on_message(filters.command("afk", PREFIX) & filters.me)
async def afk(c: CynicsCli, message: Message):
    afk_time = int(time.time())
    arg = get_arg(message)
    if not arg:
        reason = None
    else:
        reason = arg
    await Cynics.set_afk(True, afk_time, reason)
    await message.edit("**I'm going AFK**")


@CynicsCli.on_message(filters.mentioned & ~filters.bot & filters.create(user_afk), group=11)
async def afk_mentioned(c: CynicsCli, message: Message):
    global MENTIONED
    afk_time, reason = await Cynics.afk_stuff()
    afk_since = get_readable_time(time.time() - afk_time)
    if "-" in str(message.chat.id):
        cid = str(message.chat.id)[4:]
    else:
        cid = str(message.chat.id)

    if cid in list(AFK_RESTIRECT) and int(AFK_RESTIRECT[cid]) >= int(time.time()):
        return
    AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME
    if reason:
        await message.reply(
            f"**I'm AFK right now**\n**Last seen:** `(since {afk_since})`\nReason:** __{reason}__"
        )
    else:
        await message.reply(f"**I'm AFK right now**\n**Last seen:** ```(since {afk_since})```")

        _, message_type = get_message_type(message)
        if message_type == Types.TEXT:
            text = message.text or message.caption
        else:
            text = message_type.name

        MENTIONED.append(
            {
                "user": message.from_user.first_name,
                "user_id": message.from_user.id,
                "chat": message.chat.title,
                "chat_id": cid,
                "text": text,
                "message_id": message.message_id,
            }
        )


@CynicsCli.on_message(filters.create(user_afk) & filters.outgoing)
async def auto_unafk(c: CynicsCli, message: Message):
    await Cynics.set_unafk()
    unafk_message = await c.send_message(message.chat.id, "**I'm no longer AFK**")
    global MENTIONED
    text = "**Total {} mentioned you**\n".format(len(MENTIONED))
    for x in MENTIONED:
        msg_text = x["text"]
        if len(msg_text) >= 11:
            msg_text = "{}...".format(x["text"])
        text += "- [{}](https://t.me/c/{}/{}) ({}): {}\n".format(
            x["user"],
            x["chat_id"],
            x["message_id"],
            x["chat"],
            msg_text,
        )
        await c.send_message(LOG_GROUP, text)
        MENTIONED = []
    await asyncio.sleep(2)
    await unafk_message.delete()
