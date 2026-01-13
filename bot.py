# bot.py
import os
import logging
from threading import Thread
from dotenv import load_dotenv
from flask import Flask
from discord import Intents
from discord.ext import commands
from waitress import serve
from api.assign_role import assign_role_bp
from database import init_db
import keep_alive  # importamos el módulo completo para exponer `keep_alive.app`

# --- Configuración ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 3000))
DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

# --- Logging ---
if not DEBUG_MODE:
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s] %(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# --- Flask principal ---
app = Flask(__name__)
app.register_blueprint(assign_role_bp)

# --- Discord Bot ---
intents = Intents.default()
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    if DEBUG_MODE:
        logger.debug(f"Bot ready: {bot.user}")
    else:
        logger.info(f"Bot ready: {bot.user}")

# --- Funciones de arranque ---


def run_api_server():
    serve(app, host="0.0.0.0", port=PORT)


# def run_keep_alive_server():
#     serve(keep_alive.app, host="0.0.0.0", port=8080)


# --- Main ---
if __name__ == "__main__":
    init_db()
    # Thread(target=run_keep_alive_server, daemon=True).start()
    Thread(target=run_api_server, daemon=True).start()
    # bot.run(BOT_TOKEN)
