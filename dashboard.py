# Name: dcb dashboard
# Description: A dashboard for managing the dcb Discord bot.
# Author: ivar.0251 | ikoldewijn.nl

#----------------------------------#
# Imports                          #
#----------------------------------#

import json, os
from os import getenv

from botbase import Logger
from botbase.yml import create_config, ConfigObject

from quart import Quart, render_template, request, redirect, flash, session, url_for
from quart_discord import DiscordOAuth2Session

from websockets.sync.client import connect

#----------------------------------#
# Initialize environment variables #
#----------------------------------#

# Initialize environment variables from .env file
from dotenv import load_dotenv; load_dotenv()
from os import getenv

# Initialize configuration from config.yml
config: ConfigObject = create_config()

# Initialize logger for 
log = Logger("logsDashboard")

#----------------------------------#
# Defining the Dashboard App       #
#----------------------------------#

app = Quart(__name__, static_folder="static", template_folder="templates")
app.secret_key = getenv("DASHBOARD_SECRET_KEY", os.urandom(24))

app.config["DISCORD_CLIENT_ID"] = getenv("CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = getenv("CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = getenv("REDIRECT_URI")
app.config["DISCORD_BOT_TOKEN"] = getenv("BOT_TOKEN")

discord = DiscordOAuth2Session(app)

#----------------------------------#
# Blueprints                       #
#----------------------------------#

from routes.auth import create_auth_bp
app.register_blueprint(create_auth_bp(discord, log, config), url_prefix='/')


#----------------------------------#
# Websocket client                 #
#----------------------------------#

def websocket_client(data):
    with connect("ws://{}:{}".format(config.websocket_host, config.websocket_port)) as websocket:
        websocket.send(json.dumps(data))
        return json.loads(websocket.recv())

#----------------------------------#
# Running the Dashboard            #
#----------------------------------#

if __name__ == "__main__":
    app.run(
        host=config.dashboard.host,
        port=config.dashboard.port,
        debug=True
    )