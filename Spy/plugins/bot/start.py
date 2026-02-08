import time, asyncio
import random
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from Spy import app
from Spy.plugins.sudo.sudoers import sudoers_list
from Spy.utils.database import get_served_chats, get_served_users, get_sudoers
from Spy.utils import bot_sys_stats
from Spy.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from Spy.utils.decorators.language import LanguageStart
from Spy.utils.formatters import get_readable_time
from Spy.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# 🔥 FIX: BOT BOOT TIME
_boot_ = time.time()

# Images
NEXIO = [
    "https://files.catbox.moe/x5lytj.jpg",
    "https://files.catbox.moe/psya34.jpg",
    "https://files.catbox.moe/leaexg.jpg",
    "https://files.catbox.moe/b0e4vk.jpg",
    "https://files.catbox.moe/1b1wap.jpg",
    "https://files.catbox.moe/ommjjk.jpg",
    "https://files.catbox.moe/onurxm.jpg",
    "https://files.catbox.moe/97v75k.jpg",
    "https://files.catbox.moe/t833zy.jpg",
    "https://files.catbox.moe/472piq.jpg",
    "https://files.catbox.moe/qwjeyk.jpg",
    "https://files.catbox.moe/t0hopv.jpg",
    "https://files.catbox.moe/u5ux0j.jpg",
    "https://files.catbox.moe/h1yk4w.jpg",
    "https://files.catbox.moe/gl5rg8.jpg",
]

# Stickers
PURVI_STKR = [
    "CAACAgUAAxkBAAIBO2i1Spi48ZdWCNehv-GklSI9aRYWAAJ9GAACXB-pVds_sm8brMEqHgQ",
    "CAACAgUAAxkBAAIBOmi1Sogwaoh01l5-e-lJkK1VNY6MAAIlGAACKI6wVVNEvN-6z3Z7HgQ",
    "CAACAgUAAxkBAAIBPGi1Spv1tlx90xM1Q7TRNyL0fhcJAAKDGgACZSupVbmJpWW9LmXJHgQ",
    "CAACAgUAAxkBAAIBPWi1SpxJZKxuWYsZ_G06j_G_9QGkAAIsHwACdd6xVd2HOWQPA_qtHgQ",
    "CAACAgUAAxkBAAIBPmi1Sp4QFoLkZ0oN3d01kZQOHQRwAAI4FwACDDexVVp91U_1BZKFHgQ",
    "CAACAgUAAxkBAAIBP2i1SqFoa4yqgl1QSISZrQ4VuYWgAAIpFQACvTqpVWqbFSKOnWYxHgQ",
    "CAACAgUAAxkBAAIBQGi1Sqk3OGQ2jRW2rN6ZVZ7vWY2ZAAJZHQACCa-pVfefqZZtTHEdHgQ",
]

# Effect IDs
EFFECT_IDS = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]

emojis = ["🥰", "🔥", "💖", "😁", "😎", "🌚", "❤️‍🔥", "♥️", "🎉", "🙈"]


# ============================
#        START — PRIVATE
# ============================

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    # SAVE USER
    await add_served_user(message.from_user.id)

    # 🔥 FIX: Reaction safe try/except
    try:
        await message.react(random.choice(emojis))
    except:
        pass

    # Sticker animation
    sticker = await message.reply_sticker(random.choice(PURVI_STKR))
    await asyncio.sleep(1)
    await sticker.delete()

    # ---- START WITH PARAMETER ----
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        # help
        if name.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_photo(
                random.choice(NEXIO),
                has_spoiler=True,
                message_effect_id=random.choice(EFFECT_IDS),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        # sudolist
        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            return

        # info
        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "")
            query = f"https://www.youtube.com/watch?v={query}"

            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )

            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ]
                ]
            )

            await m.delete()
            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                has_spoiler=True,
                caption=searched_text,
                message_effect_id=random.choice(EFFECT_IDS),
                reply_markup=key,
            )

    # ---- NORMAL START ----
    purvi = await message.reply_text(f"<b>ʜᴇʏ ʙᴧʙʏ {message.from_user.mention} </b>")
    await asyncio.sleep(0.4)
    await purvi.edit_text("<b>ɪ ᴧᴍ ʏᴏᴜʀ ᴍᴜsɪᴄ ʙᴏᴛ..🦋</b>")
    await asyncio.sleep(0.4)
    await purvi.edit_text("<b>ʜᴏᴡ ᴧʀᴇ ʏᴏᴜ ᴛᴏᴅᴧʏ.....??</b>")
    await asyncio.sleep(0.4)
    await purvi.delete()

    out = private_panel(_)
    await message.reply_photo(
        random.choice(NEXIO),
        has_spoiler=True,
       
message_effect_id=random.choice(EFFECT_IDS),
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )


# ============================
#        START — GROUPS
# ============================

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    
    # 🔥 FIX: uptime safe
    uptime = int(time.time() - _boot_)

    await message.reply_photo(
        random.choice(NEXIO),
        has_spoiler=True,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )

    return await add_served_chat(message.chat.id)


# ============================
#          WELCOME
# ============================

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    random.choice(NEXIO),
                    has_spoiler=True, caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)