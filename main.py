# Import required libraries
import discord
import requests
import asyncio
import os

# Load environment variables from os.environ
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
HOME_ASSISTANT_URL = (os.environ.get('HOME_ASSISTANT_URL') + '/api/states/sensor.discord_status')
HOME_ASSISTANT_TOKEN = os.environ.get('HOME_ASSISTANT_TOKEN')
USER_ID = os.environ.get('USER_ID')

# Define a class to represent our Discord client
class MyClient(discord.Client):
    """
    A custom Discord client class that extends the base discord.Client class.
    It overrides two methods: on_ready and update_status.
    """

    # The on_ready method is called when the bot comes online
    async def on_ready(self):
        """
        Prints a message to the console indicating the bot has logged in successfully,
        and creates a background task to run the update_status method indefinitely.
        """
        print(f"Logged in as {self.user}")
        # Create a background task to run the update_status method every second
        self.bg_task = self.loop.create_task(self.update_status())

    # The update_status method is called every second to check for updates on the user's status
    async def update_status(self):
        """
        A loop that runs indefinitely, checking for updates on the user's status.
        It sends a POST request to Home Assistant with the current status of the user,
        and then waits 1 second before repeating.
        """
        while True:
            # Get the first server from our guilds list
            guild = self.guilds[0]
            # Try to get the member object for the specified user ID
            member = guild.get_member(USER_ID)

            # If we successfully got a member object, use its status attribute
            if member:
                status = str(member.status)
            else:
                # Otherwise, assume the user's status is unknown
                status = "unknown"

            print(f"User status: {status}")

            # Send a POST request to Home Assistant with the current status of the user
            headers = {
                "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
                "Content-Type": "application/json"
            }
            data = {"state": status, "attributes": {"friendly_name": "Discord Status"}}
            requests.post(HOME_ASSISTANT_URL, json=data, headers=headers)

            # Wait 1 second before repeating
            await asyncio.sleep(1)

# Set up our Discord client with the required intents
intents = discord.Intents.default()
intents.presences = True  # Required to track status
intents.members = True  # Required to fetch members

# Create an instance of our custom Discord client class
client = MyClient(intents=intents)
# Run the client's event loop with the provided token
client.run(DISCORD_TOKEN)