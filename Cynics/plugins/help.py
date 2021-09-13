import os
from Cynics.setclient import CynicsCli
from pyrogram import filters
from pyrogram.types import Message
from Cynics import MAX_MESSAGE_LENGTH, PREFIX
from Cynics.plugins import ALL_PLUGINS
from Cynics import HELP_COMMANDS

@CynicsCli.on_message(filters.command("help", PREFIX) & filters.me)
async def help_me(c: CynicsCli, m: Message):
    mods = ""
    mod_num = 0
    # Some Variables
    plugins = list(HELP_COMMANDS.keys())
    for plug in plugins:
        mods += f"`{plug}` "
        mod_num += 1
    all_plugins = f"<i><b>⚡Currently module loaded {mod_num}. Do {PREFIX}help <plugin_name> to get info about it.</b></i>\n\n" + mods    
    if len(m.command) == 1:
        await m.edit_text(all_plugins)
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

