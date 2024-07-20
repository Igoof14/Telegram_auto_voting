from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import GetForumTopicsRequest

# Ваши данные для подключения к API Telegram
api_id = '29630146'
api_hash = 'd1d59b2c65b2046951d638d2f6ceef73'
phone_number = '79384459654'
group_name = 'Тест подписки'  # Укажите имя вашей группы
topic_name = 'Теннис (тренировки)'  # Укажите имя вашей темы

# Подключение к Telegram
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    message = event.message
    if message.chat_id == group_id and getattr(message, 'topic_id', None) == topic_id:
        print(f"New message in topic {topic_name}: {message.text}")

async def main():
    await client.start(phone=phone_number)
    print("Connected to Telegram")

    # Получаем список всех чатов
    dialogs = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))

    group = next((chat for chat in dialogs.chats if chat.title == group_name), None)
    if not group:
        print(f"Group {group_name} not found")
        return

    topics = await client(GetForumTopicsRequest(channel=group, limit=100))
    topic = next((t for t in topics.topics if t.title == topic_name), None)
    if not topic:
        print(f"Topic {topic_name} not found in group {group_name}")
        return

    global group_id, topic_id
    group_id, topic_id = group.id, topic.id
    print(f"Listening for messages in group '{group_name}', topic '{topic_name}'")

    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
