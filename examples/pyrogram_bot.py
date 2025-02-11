import io
import base64
import requests

from typing import Any, Dict, List

from pyrogram import Client, filters, types
from pyrogram.enums.chat_member_status import ChatMemberStatus
from pyrogram.errors import RPCError

API_ID = ...
API_HASH = ...
BOT_TOKEN = ""

API_ENDPOINT = "http://127.0.0.1:1337/generate"
QUOTE_COLOR = "black"
TEXT_COLOR = "white"

app = Client(
    name="quotes_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


async def parse_messages(message: types.Message, count: int) -> List[Dict[str, Any]]:
    payloads: List[Dict[str, Any]] = []
    messages: List[types.Message] = []

    current_message_id = message.reply_to_message.id
    end_message_id = current_message_id + count

    while current_message_id < end_message_id:
        fetched_message = await app.get_messages(message.chat.id, current_message_id)
        if fetched_message:
            messages.append(fetched_message)
        current_message_id += 1

    for current_message in messages:
        user = current_message.from_user

        current_data = {
            "author": {
                "id": user.id,
                "name": current_message.from_user.first_name + (
                    " " + current_message.from_user.last_name
                    if current_message.from_user.last_name
                    else ""
                )
            }
        }

        try:
            async for photo in app.get_chat_photos(user.id, limit=1):
                avatar_bytes = await app.download_media(photo.file_id, in_memory=True)
                current_data["author"]["avatar"] = base64.b64encode(avatar_bytes.getvalue()).decode()
        except RPCError:
            pass

        current_data["text"] = current_message.text or current_message.caption or ""

        entities = current_message.entities or current_message.caption_entities or []
        if entities:
            current_data["entities"] = [
                {
                    "type": entity.type.name.lower(),
                    "offset": entity.offset,
                    "length": entity.length
                } for entity in entities
            ]

        reply = current_message.reply_to_message
        if reply:
            current_data["reply"] = {}
            current_data["reply"]["id"] = reply.from_user.id
            current_data["reply"]["name"] = reply.from_user.first_name + (
                " " + reply.from_user.last_name
                if reply.from_user.last_name
                else ""
            )
            if reply.media:
                current_data["reply"]["text"] += f"{reply.media.value}. {reply.caption or ''}"
            else:
                current_data["reply"]["text"] += reply.text or ""

        if current_message.via_bot:
            current_data["author"]["via_bot"] = current_message.via_bot.username

        if current_message.media:
            try:
                media_bytes = await app.download_media(
                    getattr(current_message, current_message.media.value),
                    in_memory=True
                )
                current_data["media"] = base64.b64encode(media_bytes.getvalue()).decode()
            except RPCError:
                pass

        try:
            chat_member_info = await message.chat.get_member(user.id)
            if chat_member_info.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                current_data["author"]["rank"] = chat_member_info.custom_title or chat_member_info.status.name.lower()
        except RPCError:
            pass

        payloads.append(current_data)

    return payloads


@app.on_message(filters.command(["quote", "q"]))
async def quote_handler(_, message: types.Message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply(
            "❌ You need to reply to a message to use this command"
        )

    count = 1
    if len(message.command) == 2 and message.command[1].isdigit():
        count = int(message.command[1])

    elif len(message.command) > 2:
        return await message.reply(
            "❌ The command must have at most 1 argument (e.g., /quote or /quote 3)"
        )

    processing_message = await message.reply("⏳ Processing messages...")

    try:
        payload = {
            "messages": await parse_messages(message, count),
            "quote_color": QUOTE_COLOR,
            "text_color": TEXT_COLOR
        }
    except Exception as error:
        return await processing_message.edit_text(
            f"❌ Error while processing messages: {error}"
        )

    await processing_message.edit_text("⏳ Waiting for API response...")

    try:
        response = requests.post(API_ENDPOINT, json=payload)
    except requests.RequestException as error:
        return await processing_message.edit_text(
            f"❌ Request error: {error}"
        )

    if response.status_code != 200:
        return await processing_message.edit_text(
            f"❌ API error [{response.status_code}]: {response.reason}"
        )

    await processing_message.edit_text("📤 Sending...")

    quote_image = io.BytesIO(response.content)
    quote_image.name = "Quote.webp"
    quote_image.seek(io.SEEK_SET)

    await app.send_sticker(
        chat_id=message.chat.id,
        sticker=quote_image,
        reply_to_message_id=reply.id
    )

    return await processing_message.delete()


if __name__ == "__main__":
    app.run()
