# Copyright (C) 2020-2021 by CandyGang@Github, < https://github.com/CandyGang >.
#
# This file is part of < https://github.com/CandyGang/Cynics > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/CandyGang/Cynics/blob/master/LICENSE >
#
# All rights reserved.

import os
from Cynics.setclient import CynicsCli
from pyrogram import filters
from pyrogram.types import Message
from Cynics import MAX_MESSAGE_LENGTH, PREFIX
from Cynics.plugins import ALL_PLUGINS
from Cynics import HELP_COMMANDS

HELP_DEFAULT = f"""
To get help for any command, just type `{PREFIX}help plugin_name`
'plugin_name' should be the name of a proper plugin!

**Get a list of all Plugins using:**
`{PREFIX}plugins`.
"""


@CynicsCli.on_message(filters.command("plugins", PREFIX) & filters.me)
async def list_plugins(c: CynicsCli, m: Message):
    # Some Variables
    mods = ""
    mod_num = 0
    # Some Variables
    plugins = list(HELP_COMMANDS.keys())
    for plug in plugins:
        mods += f"`{plug}`\n"
        mod_num += 1
    all_plugins = f"<b><u>{mod_num}</u> Modules Currently Loaded:</b>\n\n" + mods
    await m.edit_text(all_plugins)
    return


@CynicsCli.on_message(filters.command("help", PREFIX) & filters.me)
async def help_me(c: CynicsCli, m: Message):
    if len(m.command) == 1:
        await m.edit_text(HELP_DEFAULT)
    elif len(m.command) == 2:
        module_name = m.text.split(None, 1)[1]
        try:
            HELP = f"**Help for __{module_name}__**\n\n" + HELP_COMMANDS[module_name]
            await m.reply_text(HELP, parse_mode="md", disable_web_page_preview=True)
            await m.delete()
        except Exception as ef:
            await m.edit_text(f"<b>Error:</b>\n\n{ef}")
    else:
        await m.edit_text(f"Use `{PREFIX}help` to view help")
    return
