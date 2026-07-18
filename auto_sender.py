#!/usr/bin/env python3
import sys
import asyncio
from telethon import TelegramClient, sessions
from telethon.errors import FloodWaitError, RPCError

# Force logs to appear immediately (important for cloud hosts)
sys.stdout.reconfigure(line_buffering=True)

print("🚀 Worker starting...", flush=True)

# ============================================================
# 🔐 YOUR CREDENTIALS (all hardcoded)
# ============================================================
API_ID = 36705427
API_HASH = 'e69a36dc2b8c258d36d0d31c854d4aa7'
PHONE_NUMBER = '+447881257902'

# The fresh session string you generated (exclusive to this bot)
SESSION_STRING = '1BJWap1wBu3QQOAtJrzJSMTf4YO8l5lUAUHOK5-1dyOx4mPJJg1m-hN1B7jwonkKQ_gWUBGBAPtU3-BkV0_stj_qEXZBQekr4FaBlIwH2RSWkRNy8RDqudZQG6Kdmb5I3sXLIjWMch-TV9sUtgzfMTvSzjvZjNLEy1N5zky24kTWgLU2CIphHsHqtMHbu7DJOY1LJEUD1prl5l5KBVnZ1UWJyZ-H0sNY1HfyAybW-Prf7K6df9bpf5XBjAf1lHJnfnPFh94OqSaoQ1MscL6t7Q1hexLz1DgoiBStvmLKElEFR-Vxcz7H0pDkWKF8-4Kula6pUSXDdr4EsNtOyJ6DLEhTKFzbAP9M='

INVITE_LINK = 'https://t.me/+XwxJN7zdcetiNDRl'
DELAY_SECONDS = 60   # 1 minute between messages
# ============================================================

MESSAGE_TEMPLATE = """• UPI QR Generate(0.7$)
• Chat Gpt Plus 1Month On Mail($2.5)
• Netflix 1 Month on Mail (2.5$)

━━━━━━━━━
• Selling Chat Gpt Plus Method (8$)
• Selling Netflix 30days Trial Method (10$)
✅ Escrow Accepted
📩 DM to Buy @GPT_Providers"""

print("✅ Variables loaded", flush=True)


async def main():
    # Outer loop – restarts the whole client if anything fails
    while True:
        try:
            print("🔐 Connecting to Telegram...", flush=True)
            client = TelegramClient(sessions.StringSession(SESSION_STRING), API_ID, API_HASH)
            await client.start(phone=PHONE_NUMBER)
            print("✅ Logged in successfully!", flush=True)

            # Find the group
            chat = await client.get_entity(INVITE_LINK)
            print(f"✅ Target chat: {chat.title}", flush=True)

            counter = 1
            print(f"🚀 Starting send loop (every {DELAY_SECONDS}s).", flush=True)

            # Inner loop – sends messages, handles errors
            while True:
                try:
                    full_msg = f"{MESSAGE_TEMPLATE}\n\n#{counter}"
                    await client.send_message(chat, full_msg)
                    print(f"✅ Sent message #{counter}", flush=True)
                    counter += 1
                    await asyncio.sleep(DELAY_SECONDS)
                except FloodWaitError as e:
                    print(f"⏳ Flood wait: {e.seconds}s", flush=True)
                    await asyncio.sleep(e.seconds)
                except (ConnectionError, RPCError) as e:
                    print(f"⚠️ Connection lost: {e}. Reconnecting...", flush=True)
                    break  # exit inner loop to reconnect
                except Exception as e:
                    print(f"⚠️ Unexpected error in send loop: {e}", flush=True)
                    await asyncio.sleep(10)
                    break  # exit inner loop to reconnect

            await client.disconnect()
            print("🔄 Disconnected. Reconnecting in 10s...", flush=True)
            await asyncio.sleep(10)

        except Exception as e:
            print(f"💥 Fatal error in main loop: {e}", flush=True)
            await asyncio.sleep(30)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Stopped by user.", flush=True)
    except Exception as e:
        print(f"💥 Critical error: {e}", flush=True)
        sys.exit(1)
