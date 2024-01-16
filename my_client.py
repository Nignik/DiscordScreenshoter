import discord
import os
from dotenv import load_dotenv
from discord.ext import tasks, commands
import pyautogui
import datetime
import asyncio


class MyClient(discord.Client):
    def __init__(self, intents, channel):
        super().__init__(intents=intents)
        load_dotenv()
        self.channel = channel
        self.image_dir_path = os.getenv('SCREENSHOTS_FOLDER')

    async def on_ready(self):
        self.channel = self.get_channel(int(self.channel))
        self.send_screenshot.start()

    @tasks.loop(minutes=5)
    async def send_screenshot(self):
        channel = self.channel
        image_path = await self.take_screenshot()
        if channel:
            await self.send_image(channel, image_path)

    @staticmethod
    async def send_image(channel, image_path):
        if os.path.exists(image_path):
            await channel.send(file=discord.File(image_path))

    async def take_screenshot(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._take_screenshot_sync)

    def _take_screenshot_sync(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        file_path = os.path.join(self.image_dir_path, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        print(f"Screenshot taken and saved as {file_path}")
        return file_path
