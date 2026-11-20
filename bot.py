# Initialize environment variables from .env file
from dotenv import load_dotenv; load_dotenv()
from os import getenv

#----------------------------------#
# Imports
#----------------------------------#

from nextcord import Embed, Intents, Interaction
from nextcord.ext import commands

from botbase import Logger, random_color
from botbase.yml import create_config, ConfigObject

#----------------------------------#
# Initialize environment variables
#----------------------------------#

# Initialize environment variables from .env file
from dotenv import load_dotenv; load_dotenv()
from os import getenv

# Initialize configuration from config.yml
config: ConfigObject = create_config()

# Initialize logger for 
log = Logger("logs")

class Bot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=config.bot.default_command_prefix, intents=intents)

    async def on_ready(self):
        log.info("Logged in as {} ({})".format(self.user.name, self.user.id))

bot = Bot()

if __name__ == "__main__":
    bot.run(getenv("BOT_TOKEN"))