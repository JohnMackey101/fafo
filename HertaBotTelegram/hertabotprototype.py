import asyncio
import re
from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest

api_id = "YOURAPPID"
api_hash = 'YOURTELEGRAMHASH"
phone_number = 'YOURPHOnENUMBER'
# Regex to capture invite links like:
#   https://t.me/joinchat/AAAAAECFJz_uvvAAA
#   https://t.me/+AAAAAECFJz_uvvAAA
invite_pattern = re.compile(r'(?:https?://)?t\.me/(?:joinchat/|\+)([\w_-]+)')

client = TelegramClient("user_session", api_id, api_hash)



@client.on(events.NewMessage)
async def auto_join_handler(event):
    # 1) Parse message to find an invite link
    match = invite_pattern.search(event.raw_text)
    if match:
        invite_hash = match.group(1)
        # 2) IMMEDIATELY try to join
        try:
            await client(ImportChatInviteRequest(invite_hash))
        except Exception as e:
            # (Optional) Log or print the error, but do *not* reply or do big tasks.
            print(f"Failed to join {invite_hash}: {e}")

async def main():
    # Start up the Telethon client (log in the first time)
    await client.start(phone=phone_number)
    print("Userbot is running. Waiting for invite links...")

with client:
    # We use run_until_complete to start up the client, then run_until_disconnected 
    # keeps listening for incoming messages/events.
    client.loop.run_until_complete(main())
    client.run_until_disconnected()