import nextcord; from nextcord.ext import commands
from botbase.yml import create_config, ConfigObject; config: ConfigObject = create_config()
from sqlite3 import Connection

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot, db: Connection):
        self.bot = bot
        self.db = db

    def __get_help_embed(self):
        embed = nextcord.Embed(
            title="Help Information",
            description="Here is some help information about the bot.",
            color=nextcord.Color.blue()
        )
        for command in config.commands.__dict__.values():
            embed.add_field(name=command.name.capitalize(), value=f"{command.description}\nUsage: `{command.usage}`", inline=False)
        return embed

    @nextcord.slash_command(name=config.commands.help.name, description=config.commands.help.description)
    async def help(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=self.__get_help_embed())

    @commands.command(name=config.commands.help.name, help=config.commands.help.description)
    async def help_command(self, ctx: commands.Context):
        await ctx.send(embed=self.__get_help_embed())

def setup(bot):
    bot.add_cog(HelpCog(bot))