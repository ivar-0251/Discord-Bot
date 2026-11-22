import nextcord; from nextcord.ext import commands
from botbase.yml import create_config, ConfigObject; config: ConfigObject = create_config()
from botbase import Logger; log = Logger("logs")
from botbase import random_color
from sqlite3 import Connection

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot, db: Connection):
        self.bot = bot
        self.db = db

    def __get_help_embed(self) -> nextcord.Embed:
        embed = nextcord.Embed(
            color=self.__get_current_color()
        )
        if self.__get_current_language() == "en":
            embed.title = "Help Information"
            embed.description = "Here is some help information about the bot."

            for command in config.commands.__dict__.values():
                embed.add_field(name=command.name.capitalize(), value=f"{command.description_en}\nUsage: `{command.usage}`", inline=False)
            return embed
        if self.__get_current_language() == "nl":
            embed.title = "Hulpinformatie"
            embed.description = "Hier is wat hulpinformatie over de bot."

            for command in config.commands.__dict__.values():
                embed.add_field(name=command.name.capitalize(), value=f"{command.description_nl}\nGebruik: `{command.usage}`", inline=False)
            return embed


    def __get_current_language(self) -> str:
        # Placeholder for actual language retrieval logic
        return config.bot.default_language

    def __get_current_color(self) -> int:
        return random_color() if config.bot.default_color == "random" else int(str(config.bot.default_color).replace("#", ""), 16)

    @nextcord.slash_command(name=config.commands.help.name, description=config.commands.help.description_en)
    async def help(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=self.__get_help_embed())

    @commands.command(name=config.commands.help.name, help=config.commands.help.description_en)
    async def help_command(self, ctx: commands.Context):
        await ctx.send(embed=self.__get_help_embed())