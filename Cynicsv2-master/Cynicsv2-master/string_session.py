import asyncio
from configparser import ConfigParser, NoOptionError, NoSectionError

from pyrogram import Client

config = ConfigParser()
try:
    config.read("config.ini")
    APP_ID = config.getint("Enterprise", "APP_ID")
    API_HASH = config.get("Enterprise", "API_HASH")
except (NoOptionError, NoSectionError):
    APP_ID = int(input("enter Telegram APP ID: "))
    API_HASH = input("enter Telegram API HASH: ")


async def main(app_id, api_hash):
    """generate StringSession for the current MemorySession"""
    async with Client(":memory:", api_id=APP_ID, api_hash=API_HASH) as app:
        await app.send_message(
            "me", f"#STRING_SESSION\n\n```{await app.export_session_string()}``` **TAP TO COPY\nJoin @CynicsUserbot For Help!**"
        )
        print("Done !, session string has been sent to saved messages!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(APP_ID, API_HASH))
