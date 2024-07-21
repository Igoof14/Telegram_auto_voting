import os
from time import sleep

from dotenv import load_dotenv
from telethon import TelegramClient, events
import logging

from telethon.tl.functions.messages import SendVoteRequest
from telethon.tl.types import MessageMediaPoll

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')
session_name = os.getenv('SESSION_NAME')
group_id = int(os.getenv('GROUP_ID'))
thread_id = int(os.getenv('THREAD_ID'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient(session_name, api_id, api_hash)


@client.on(events.NewMessage(chats=group_id))
async def handler(event):
    message = event.message
    try:
        if (message.reply_to.reply_to_msg_id == thread_id
                and isinstance(message.media, MessageMediaPoll)):
            poll = message.media.poll
            if ('НТЦ' in poll.question.text or 'МТА' in poll.question.text) \
                    and 'допкорт' not in poll.question.text.lower():
                for answer in poll.answers:
                    if 'новички' in answer.text.text.lower().strip():
                        sleep(1)
                        await client(SendVoteRequest(
                            peer=message.peer_id,
                            msg_id=message.id,
                            options=[answer.option]
                        ))
                        break
    except:
        pass


async def main():
    await client.start(phone)
    logger.info("Bot started and listening for new messages in the thread.")
    await client.run_until_disconnected()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
