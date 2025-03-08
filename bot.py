import discord
import requests
import os
from dotenv import load_dotenv
from flask import Flask

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# Servidor Flask para mantener Vercel activo
app = Flask(__name__)

@app.route("/")
def home():
    return "El bot está corriendo."

def traducir_texto(texto, idioma_destino):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": texto,
        "target_lang": idioma_destino
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        return None

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    contenido = message.content
    idioma_origen = None
    idioma_destino = None

    if contenido.isascii():
        idioma_origen = "ES"
        idioma_destino = "IT"
    else:
        idioma_origen = "IT"
        idioma_destino = "ES"

    traduccion = traducir_texto(contenido, idioma_destino)

    if traduccion:
        await message.channel.send(f"**{message.author.name}**: {traduccion}")

# Iniciar bot de Discord y servidor Flask
if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: client.run(TOKEN)).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
