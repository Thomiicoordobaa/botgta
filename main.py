import discord
from discord.ext import commands
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

FICHAS_FILE = "fichas.json"
symbols = ["🍒", "🍋", "🍇", "🔔", "⭐", "7️⃣"]

# Cargar fichas desde archivo JSON
def cargar_fichas():
    if not os.path.isfile(FICHAS_FILE):
        with open(FICHAS_FILE, "w") as f:
            json.dump({}, f)
    with open(FICHAS_FILE, "r") as f:
        return json.load(f)

# Guardar fichas en archivo JSON
def guardar_fichas(fichas):
    with open(FICHAS_FILE, "w") as f:
        json.dump(fichas, f, indent=4)

# Comando para mostrar fichas del usuario
@bot.command()
async def fichas(ctx):
    fichas_data = cargar_fichas()
    user_id = str(ctx.author.id)
    cantidad = fichas_data.get(user_id, 0)
    await ctx.send(f"{ctx.author.mention}, tienes {cantidad} fichas.")

# Comando para transferir fichas (admin)
@bot.command()
@commands.has_permissions(administrator=True)
async def transferir(ctx, usuario: discord.Member, cantidad: int):
    if cantidad <= 0:
        return await ctx.send("La cantidad debe ser mayor a 0.")

    fichas_data = cargar_fichas()
    admin_id = str(ctx.author.id)
    destino_id = str(usuario.id)

    fichas_data[admin_id] = fichas_data.get(admin_id, 0)
    fichas_data[destino_id] = fichas_data.get(destino_id, 0)

    if fichas_data[admin_id] < cantidad:
        return await ctx.send("No tienes suficientes fichas para transferir.")

    fichas_data[admin_id] -= cantidad
    fichas_data[destino_id] +=