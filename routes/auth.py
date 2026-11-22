from quart import Blueprint, redirect, render_template, request, session, url_for
from quart_discord import DiscordOAuth2Session
from botbase import Logger, ConfigObject

def create_auth_bp(discord: DiscordOAuth2Session, log: Logger, config: ConfigObject):
    auth_bp = Blueprint("auth", __name__)

    @auth_bp.route('/login')
    async def login():
        next_url = (request.args.get("next") or "").strip()
        if next_url and next_url.startswith("/") and not next_url.startswith("//"):
            session["post_login_redirect"] = next_url

        if not await discord.authorized:
            return await discord.create_session(scope=["identify", "guilds"])
        post_login_redirect = session.pop("post_login_redirect", None)
        if isinstance(post_login_redirect, str) and post_login_redirect.startswith("/") and not post_login_redirect.startswith("//"):
            return redirect(post_login_redirect)

        return redirect(url_for("dashboard"))

    @auth_bp.route("/callback")
    async def callback():
        try:
            await discord.callback()
        except Exception as e:
            log.error(f"Error during Discord OAuth2 callback:\n{e}")
            return "An error occurred during login attempt. Please try again."
        user = await discord.fetch_user()

        post_login_redirect = session.pop("post_login_redirect", None)
        if isinstance(post_login_redirect, str) and post_login_redirect.startswith("/") and not post_login_redirect.startswith("//"):
            return redirect(post_login_redirect)

        return redirect(url_for("dashboard"))

    @auth_bp.route("/logout")
    async def logout():
        if await discord.authorized:
            discord.revoke()
        
        return redirect(url_for("index"))

    return auth_bp