import discord
from discord.ext import commands
import wolframalpha
import private as pri

client = discord.Client()
client = commands.Bot(command_prefix="i")

@client.event
async def on_ready():
    print("Im on.")

@client.command()
async def mup(ctx):
    await ctx.send("Im ready.")

@client.command()
async def math(ctx, *, question):
    math = wolframalpha.Client(pri.Wolframaplha_API)
    resQ = math.query(str(question))
    # print(next(resQ.title).text)
    answer = next(resQ.results).text

    e = discord.Embed(color=0x7289da, title = f"{answer}")
    e.set_footer(text= f'Requested by {ctx.author}' , icon_url=ctx.author.avatar_url)
    await ctx.send(embed = e)



client.run(pri.Bot_Token)