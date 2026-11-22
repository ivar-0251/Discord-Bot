# Name: dcb
# Description: A Discord bot for various utilities and fun commands.
# Author: ivar.0251 | ikoldewijn.nl

#----------------------------------#
# Imports                          #
#----------------------------------#

from nextcord import Embed, Intents, Interaction
from nextcord.ext import commands

from botbase import Logger, random_color
from botbase.yml import create_config, ConfigObject

import sqlite3 as sql
import json, sys, asyncio, os

from websockets.legacy.server import serve

#----------------------------------#
# Initialize environment variables #
#----------------------------------#

# Initialize environment variables from .env file
from dotenv import load_dotenv; load_dotenv()
from os import getenv

# Initialize configuration from config.yml
config: ConfigObject = create_config()

# Initialize logger for 
log = Logger("logs")

#----------------------------------#
# Defining the Bot                 #
#----------------------------------#

class Bot(commands.Bot):
    def __init__(self):
        self._intents = Intents.default()
        self._intents.message_content = True

        super().__init__(command_prefix=config.bot.default_command_prefix, intents=self._intents, help_command=None)

        self.db = sql.connect(config.database_file_name)
        cursor = self.db.cursor()
        # Create the database table if it doesn't exist

        self.db.commit()
        cursor.close()
        log.debug("Database connection established.")

    async def on_ready(self):
        log.info("Logged in as {} ({})".format(self.user.name, self.user.id))

bot = Bot()

#----------------------------------#
# Loading Cogs                     #
#----------------------------------#

from cogs.help import HelpCog
bot.add_cog(HelpCog(bot, bot.db))

#----------------------------------#
# WebSocket Server                 #
#----------------------------------#

# Listen for incoming WebSocket connections
async def websocket_handler(websocket):
    async for message in websocket:
        data: dict = json.loads(message)
        log.debug("Received WebSocket message with type: {}".format(data["type"]))

        # await websocket.send(json.dumps())

# Create a function to start the WebSocket server
async def main():
    async with serve(websocket_handler, config.websocket_host, config.websocket_port):
        log.info("WebSocket server started on ws://{}:{}".format(config.websocket_host, config.websocket_port))
        await asyncio.Future()  # Run forever

#----------------------------------#
# Running the Bot                  #
#----------------------------------#

async def run_all():
    await asyncio.gather(
        main(),
        bot.start(getenv("BOT_TOKEN"))
    )

if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except KeyboardInterrupt:
        log.warning("Bot is shutting down...")
        sys.exit(0)