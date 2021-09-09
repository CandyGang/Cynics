import time
import os
from io import BytesIO
from platform import python_version
from Cynics.setclient import CynicsCli
from pyrogram import filters, __version__
from pyrogram.types import Message
from Cynics import PREFIX, OWNER_NAME, CYNICS_VERSION, UPSTREAM_REPO
from pyrogram.raw.all import layer
from Cynics.helpers.clear_strings import clear_string

# -- Constants -- #
ALIVE_TEXT = (
    "<b>✨ [Cynics]({}):</b>\n"
    "<b> - Owner:</b> `{}`\n"
    "<b> - Pyrogram Version:</b> `{}`\n"
    "<b> - Python Version:</b> `{}`\n"
    "<b> - Cynics Version:</b> `{}`\n\n"
)
# -- Constants End -- #

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Basic Commands of Userbot!

`{PREFIX}alive` / `{PREFIX}start`: Check if bot is alive or not.
`{PREFIX}ping`: Get pinged.
`{PREFIX}id`: Get the ID of the file/user/group.
`{PREFIX}json`: Get json of the replied message.
"""


@CynicsCli.on_message(
    filters.command(["alive", "start"], PREFIX) & filters.me
)
async def check_alive(c: CynicsCli, m: Message):
    await m.edit_text(
        ALIVE_TEXT.format(
            UPSTREAM_REPO,
            OWNER_NAME,
            __version__,
            python_version(),
            CYNICS_VERSION,
        ),
        disable_web_page_preview=True,
    )


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
        await m.reply_text(f"<code>{the_real_message}</code>")
    except Exception as e:
        OUTPUT = clear_string(the_real_message)  # Remove the html elements using regex
        with BytesIO(str.encode(OUTPUT)) as f:
            f.name = "json.txt"
            await m.reply_document(document=f, caption=str(e))
        await m.delete()
    return
