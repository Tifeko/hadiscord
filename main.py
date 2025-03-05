import discord
import requests
import asyncio
import os

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
HOME_ASSISTANT_URL = (os.environ.get('HOME_ASSISTANT_URL') + '/api/states/sensor.discord_status')
HOME_ASSISTANT_TOKEN = os.environ.get('HOME_ASSISTANT_TOKEN')
USER_ID = os.environ.get('USER_ID')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.bg_task = self.loop.create_task(self.update_status())

    async def update_status(self):
        while True:
            guild = self.guilds[0]  # Get the first server
            member = guild.get_member(USER_ID)  # Get the member object

            if member:
                status = str(member.status)
            else:
                status = "unknown"

            print(f"User status: {status}")

            # Send status to Home Assistant
            headers = {
                "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
                "Content-Type": "application/json"
            }
            data = {"state": status, "attributes": {"friendly_name": "Discord Status"}}
            requests.post(HOME_ASSISTANT_URL, json=data, headers=headers)

            await asyncio.sleep(1)  # Check every second

intents = discord.Intents.default()
intents.presences = True  # Required to track status
intents.members = True  # Required to fetch members

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
