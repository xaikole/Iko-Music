import asyncio
from datetime import datetime, timedelta
from pyrogram.enums import ChatType

import config
from ANNIEMUSIC import app
from ANNIEMUSIC.core.call import JARVIS, autoend
from ANNIEMUSIC.utils.database import is_active_chat, is_autoend

# Menyimpan waktu untuk auto leave
auto_leave_timers = {}

async def auto_leave():
    while True:
        await asyncio.sleep(5)  # Periksa setiap 5 detik
        current_time = datetime.now()
        for chat_id, leave_time in list(auto_leave_timers.items()):
            if current_time >= leave_time:
                try:
                    await JARVIS.leave_chat(chat_id)
                    await app.send_message(chat_id, "» Asisten secara otomatis meninggalkan video chat karena tidak ada aktivitas.")
                    await app.leave_chat(chat_id)  # Keluar dari grup juga
                except Exception as e:
                    print(f"Error leaving chat {chat_id}: {e}")
                del auto_leave_timers[chat_id]  # Hapus timer setelah keluar

async def auto_end():
    while True:
        await asyncio.sleep(5)
        ender = await is_autoend()
        if not ender:
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    auto_leave_timers[chat_id] = datetime.now() + timedelta(seconds=180)  # Set timer untuk 180 detik
                    continue
                autoend[chat_id] = {}
                try:
                    await JARVIS.stop_stream(chat_id)
                    await app.send_message(
                        chat_id,
                        "» ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʟᴇғᴛ ᴠɪᴅᴇᴏᴄʜᴀᴛ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.",
                    )
                except Exception as e:
                    print(f"Error during auto end in chat {chat_id}: {e}")

asyncio.create_task(auto_leave())
asyncio.create_task(auto_end())
