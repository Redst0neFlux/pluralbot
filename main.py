import discord
from discord.ext import commands
from discord import app_commands
from collections import defaultdict

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

identities = defaultdict(dict)
active = {}

@tree.command(
    name="say", description="Says a message as current identity", guild=discord.Object(id=719281356622004297)
)
async def say(ctx, message: str):
    name = active[ctx.user.id]
    image_url = identities[ctx.user.id][name]
    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        if webhook.name == "PluralBot":
            break
    else:
        webhook = await ctx.channel.create_webhook(name="PluralBot")
    await ctx.response.send_message(":e_mail:", ephemeral=True)
    await webhook.send(content=message, avatar_url=image_url, username=name)

@tree.command(
    name="create", description="Create a new identity", guild=discord.Object(id=719281356622004297)
)
async def create(ctx: discord.Interaction, name: str, image_url: str):
    identities[ctx.user.id][name] = image_url
    await ctx.response.send_message(f"Created identity {name}", ephemeral=True)

@tree.command(
    name="swap", description="Changes active identity", guild=discord.Object(id=719281356622004297)
)
async def swap(ctx:discord.Interaction, name: str):
    if name in identities[ctx.user.id].keys():
        active[ctx.user.id] = name
        await ctx.response.send_message(f"Swapped to {name}", ephemeral=True)
    else:
        await ctx.response.send_message("Error", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=719281356622004297))
    print("Ready!")


with open("token.txt", "r") as t:
    token = t.read()

client.run(token)
