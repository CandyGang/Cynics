import os
from datetime import datetime

from pyrogram import filters
from pyrogram.types import User, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid
from Cynics.setclient import CynicsCli
from Cynics import PREFIX

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""

`{PREFIX}whois` / `{PREFIX}info`: Extract user data with help of Ub
"""

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


infotext = (
    "**[{full_name}](tg://user?id={user_id})**\n"
    " > **UserID:** `{user_id}`\n"
    " > **First Name:** `{first_name}`\n"
    " > **Last Name:** `{last_name}`\n"
    " > **Username:** @{username}\n"
    " > **DC:** {dc_id}\n"
    " > **Status:** {status}\n"
    " > **Is Scam:** {scam}\n"
    " > **Is Bot:** {bot}\n"
    " > **Is Verified:** {verifies}\n"
    " > **Is Contact:** {contact}\n"
    " > **Total Groups In Common:** {common}"
)


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@CynicsCli.on_message(filters.command(["whois", "info"], PREFIX) & filters.me)
async def whois(c: CynicsCli, message: Message):
    await message.edit_text("`Extracting User Data...`")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await c.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("I don't know that User.")
        return
    common = await c.get_common_chats(user.id)
    pfp = await c.get_profile_photos(user.id)
    if not pfp:
        await message.edit_text(
            infotext.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name or "",
                username=user.username or "",
                dc_id=user.dc_id or "1",
                status=user.status or "None",
                scam=user.is_scam,
                bot=user.is_bot,
                verifies=user.is_verified,
                contact=user.is_contact,
                common=len(common),
            ),
            disable_web_page_preview=True,
        )
    else:
        dls = await c.download_media(pfp[0]["file_id"], file_name=f"{user.id}.png")
        await message.delete()
        await c.send_document(
            message.chat.id,
            dls,
            caption=infotext.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name or "",
                username=user.username or "",
                dc_id=user.dc_id or "1",
                status=user.status or "None",
                scam=user.is_scam,
                bot=user.is_bot,
                verifies=user.is_verified,
                contact=user.is_contact,
                common=len(common),
            ),
            reply_to_message_id=message.reply_to_message.message_id
            if message.reply_to_message
            else None,
        )
        os.remove(dls)
