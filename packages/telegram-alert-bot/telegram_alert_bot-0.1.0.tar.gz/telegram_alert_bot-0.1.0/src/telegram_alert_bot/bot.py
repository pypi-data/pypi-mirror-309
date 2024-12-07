import asyncio
import logging
from telegram import Bot #type: ignore
from telegram.error import TelegramError #type: ignore

class TelegramAlertBot:
    def __init__(self, token: str, user_id: str):
        self.token = token
        self.user_id = user_id
        self.message_queue = asyncio.Queue()
        
    async def send_telegram_message(self, message: str):
        bot = Bot(token=self.token)
        try:
            await bot.send_message(chat_id=self.user_id, text=message)
            logging.info(f"Sent message: {message}")
        except TelegramError as e:
            logging.error(f"Error sending message: {e}")

    async def background_bot_polling(self):
        logging.info("Starting Telegram bot polling...")
        while True:
            message = await self.message_queue.get()
            if message:
                await self.send_telegram_message(message)
            self.message_queue.task_done()

    async def event_trigger(self, message: str, bot: str):
        message += f"\n@{bot}"
        logging.info(f"Event triggered! Queueing message: {message}")
        await self.message_queue.put(message) 