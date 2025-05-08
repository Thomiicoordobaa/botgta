import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import random
import os

TOKEN = os.getenv("TOKEN")  # Toma el token desde las "Secrets"

intents = discord.Intents.default()
intents.message_content = True  # Habilita el intent de contenido de mensaje
bot = commands.Bot(command_prefix='!', intents=intents)

def generar_dni(nombre, apellido, edad, nacionalidad):
    try:
        dni = Image.new('RGB', (400, 250), color=(200, 200, 200))
        draw = ImageDraw.Draw(dni)
        font = ImageFont.load_default()
        draw.text((20, 20), f"Nombre: {nombre}", font=font, fill="black")
        draw.text((20, 60), f"Apellido: {apellido}", font=font, fill="black")
        draw.text((20, 100), f"Edad: {edad}", font=font, fill="black")
        draw.text((20, 140), f"Nacionalidad: {nacionalidad}", font=font, fill="black")
        draw.text((20, 180), f"DNI Nº: {random.randint(10000000, 99999999)}", font=font, fill="black")
        ruta = f"dni_{random.randint(1000, 9999)}.png"
        dni.save(ruta)
        return ruta
    except Exception as e:
        print(f"Error al generar DNI: {e}")
        return None

@bot.command()
async def dni(ctx, nombre, apellido, edad: int, nacionalidad):
    print("Comando !dni ejecutado")
    ruta = generar_dni(nombre, apellido, edad, nacionalidad)
    if ruta is not None:
        try:
            file = discord.File(ruta, filename="dni.png")
            await ctx.send("Aquí está tu DNI:", file=file)
            os.remove(ruta)
        except Exception as e:
            print(f"Error al enviar archivo: {e}")
            await ctx.send("Ocurrió un error al enviar el archivo")
    else:
        await ctx.send("Ocurrió un error al generar el DNI")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

bot.run(TOKEN)