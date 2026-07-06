import os
import time
import random
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError

# Configuration
api_id = '36576852'  # Replace with your API ID
api_hash = '2c6ad07f8ffa50edf8b110d713b40df9'  # Replace with your API Hash
phone = '+998912188809'  # Replace with your phone number
session_name = 'telegrambot'  # Session name for Telethon
ad_message = '💋 Real qizlar bor Pastayankala bor'  # Replace with your ad message
delay = 3600  # Delay between sending messages in seconds (1 hour)

# Initialize the client
client = TelegramClient(session_name, api_id, api_hash)

async def get_groups():
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    chats = []
    for chat in result.chats:
        try:
            if chat.megagroup == True:
                chats.append(chat)
        except:
            continue
    return chats

async def send_ad_to_groups():
    try:
        await client.start(phone)
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, '12345')  # Enter the code: 12345
        groups = await get_groups()
        for group in groups:
            try:
                await client.send_message(group, ad_message)
                print(f"Message sent to {group.title}")
            except PeerFloodError:
                print("Getting Flood Error from Telegram. Script is stopping now.")
                print("Please try again after some time.")
                break
            except UserPrivacyRestrictedError:
                print(f"User privacy restricted for {group.title}. Skipping.")
                continue
            except Exception as e:
                print(f"Error sending message to {group.title}: {e}")
                continue
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def main():
    while True:
        await send_ad_to_groups()
        print("Waiting for the next cycle...")
        time.sleep(delay)  # Removed to start the next cycle immediately

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
