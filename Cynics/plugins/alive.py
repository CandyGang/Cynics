import time
import os
from io import BytesIO
from datetime import datetime
from platform import python_version
from Cynics.setclient import CynicsCli
from pyrogram import filters, __version__
from pyrogram.types import Message
from Cynics import PREFIX, OWNER_NAME, CYNICS_VERSION, UPSTREAM_REPO, StartTime
from pyrogram.raw.all import layer
from Cynics.helpers.clear_strings import clear_string

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Basic Commands of Userbot!

`{PREFIX}alive`/`{PREFIX}start`: Check if bot is alive or not.
`{PREFIX}ping`: Get pinged.
`{PREFIX}id`: Get the ID of the file/user/group.
`{PREFIX}json`: Get json of the replied message.
"""


@CynicsCli.on_message(
    filters.command(["alive", "start"], PREFIX) & filters.me
)
async def check_alive(c: CynicsCli, m: Message):
    alive_img = "https://telegra.ph/file/4718cbed7c63bd52031a4.jpg"
    alive_str = f"""
「**[Cynics-UserBot]({UPSTREAM_REPO})**」 **is Alive!!**
**Owner**: `{OWNER_NAME}`
**Version**: `{CYNICS_VERSION}`
**PyroGram Version**: `{__version__}`
**Uptime**: `{str(datetime.now() - StartTime).split('.')[0]}`
**Python Version**: `3.9.6`
"""    
    await m.delete()
    if m.reply_to_message:
        await c.send_photo(
            m.chat.id,
            alive_img,
            caption=alive_str,
            reply_to_message_id=m.reply_to_message.message_id,
        )
    else:
        await c.send_photo(m.chat.id, alive_img, caption=alive_str)


@CynicsCli.on_message(
    filters.command("repo", PREFIX) & filters.me
)
async def repo(c: CynicsCli, message: Message):
    repo = "Official Source Code Of [Cynics](https://github.com/CandyGang/Cynics.git)"
    await message.edit_text(repo, disable_web_page_preview=True)


@CynicsCli.on_message(filters.command("id", PREFIX) & filters.me)
async def get_id(c: CynicsCli, m: Message):
    file_id = None
    user_id = None

    if m.reply_to_message:
        rep = m.reply_to_message
        if rep.audio:
            file_id = rep.audio.file_id
        elif rep.document:
            file_id = rep.document.file_id
        elif rep.photo:
            file_id = rep.photo.file_id
        elif rep.sticker:
            file_id = rep.sticker.file_id
        elif rep.video:
            file_id = rep.video.file_id
        elif rep.animation:
            file_id = rep.animation.file_id
        elif rep.voice:
            file_id = rep.voice.file_id
        elif rep.video_note:
            file_id = rep.video_note.file_id
        elif rep.contact:
            file_id = rep.contact.file_id
        elif rep.location:
            file_id = rep.location.file_id
        elif rep.venue:
            file_id = rep.venue.file_id
        elif rep.from_user:
            if rep.forward_from:
                user_id = rep.forward_from.id
                if rep.forward_from.last_name:
                    user_name = (
                        rep.forward_from.first_name + " " + rep.forward_from.last_name
                    )
                else:
                    user_name = rep.forward_from.first_name
                username = rep.forward_from.username
            else:
                user_id = rep.from_user.id
                if rep.from_user.last_name:
                    user_name = rep.from_user.first_name + " " + rep.from_user.last_name
                else:
                    user_name = rep.from_user.first_name
                username = rep.from_user.username

    if user_id:
        await m.edit_text(
            "**User ID:** `{}`\n**Name:** `{}`\n**Username:** @{}".format(
                user_id, user_name, username
            )
        )
    elif file_id:
        await m.edit_text(f"**File's ID:** `{file_id}`")
    else:
        await m.edit_text(f"**This Chat's ID:** `{m.chat.id}`")


@CynicsCli.on_message(filters.command("json", PREFIX) & filters.me)
async def jsonify(c: CynicsCli, m: Message):
    the_real_message = None
    reply_to_id = None

    if m.reply_to_message:
        the_real_message = m.reply_to_message
    else:
        the_real_message = m
    try:
        await m.edit_text(f"<code>{the_real_message}</code>")
    except Exception as e:
        OUTPUT = clear_string(the_real_message)  # Remove the html elements using regex
        with BytesIO(str.encode(OUTPUT)) as f:
            f.name = "json.txt"
            await m.reply_document(document=f, caption=str(e))
        await m.delete()
    return

@CynicsCli.on_message(filters.command("save", PREFIX) & filters.me)
async def to_saved(c: CynicsCli, message: Message):
    await message.reply_to_message.forward("self")
    await message.edit_text('`Saved message.`')

@CynicsCli.on_message(filters.command(["uptime", "up"], PREFIX) & filters.me)
async def uptime(c: CynicsCli, message: Message):
    uptime = f"**Current Uptime:** `{str(datetime.now() - StartTime).split('.')[0]}`"
    await message.edit_text(uptime)

