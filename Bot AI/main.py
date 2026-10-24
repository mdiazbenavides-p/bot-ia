import discord
from discord.ext import commands
from model import get_class
import os, random
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Función que obtiene una imagen aleatoria desde la API
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

# NUEVA FUNCIÓN: Permite guardar imágenes adjuntas por el usuario
async def save_user_image(attachment, save_dir="./images"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = os.path.join(save_dir, attachment.filename)
    await attachment.save(file_path)
    return file_path


@bot.command('duck')
async def duck(ctx):
    '''Si el usuario adjunta una imagen la guarda; si no, devuelve una aleatoria'''
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_path = await save_user_image(attachment)
            await ctx.send(f"¡Imagen de pato guardada con éxito en `{file_path}`!")
    else:
        print('hello')
        image_url = get_duck_image_url()
        await ctx.send(image_url)


@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=f"./{attachment.filename}"))
    else:
        await ctx.send("You forgot to upload the image :(")

bot.run("MTU2MTA1MzMyNDg0Nzg3NDEzOA.GrArBF.49fv-GQfioCKGju7Kc7iQJ8oWHWKfebAmq_8xI")