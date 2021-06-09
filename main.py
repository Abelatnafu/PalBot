import discord
from discord.ext import commands
import wolframalpha
import googletrans
from dotenv import load_dotenv
import os

load_dotenv()


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
    math = wolframalpha.Client(os.environ.get('Wolframaplha_API'))
    resQ = math.query(str(question))
    # print(next(resQ.title).text)
    answer = next(resQ.results).text

    e = discord.Embed(color=0x7289da, title = f"{answer}")
    e.set_footer(text= f'Requested by {ctx.author}' , icon_url=ctx.author.avatar_url)
    await ctx.send(embed = e)


@client.command(aliases = ["tran"])
async def translate(ctx,lang_to,*,argument):


            #language tp translate to needs to be lowercase to find it in the google trans language dictionary
    lang_to = lang_to.lower()

            # Chinese has 2different languges(simplified and traditional) so doesn't recognize just chinese so to make the simplified default
    if lang_to == "chinese":
        lang_to = "zh-cn"

    # print(googletrans.LANGUAGES)

            #Check if the languge we are translating too is found in the list
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Can't find the languages you are trying to translate to.")

            # initialize google translator
    translator = googletrans.Translator()

            # translate given argument into given languge
    transed = translator.translate(argument, dest=lang_to)
    # print(transed.extra_data["synonyms"])

            #If it has no pronunciation or the same as argument
    if transed.pronunciation == None or transed.pronunciation == argument:
        pronunciation = "---"
            #if it has a pronunciation then get it
    else:
        pronunciation = transed.pronunciation

            #embed the information in a box to send it
    e = discord.Embed(color=0x7289da, title=f"{transed.text} \nPronounced '{pronunciation}'")
    imageAdd = "https://cdn3.iconfinder.com/data/icons/google-suits-1/32/18_google_translate_text_language_translation-512.png"
    e.set_footer(text="Google translate", icon_url=imageAdd)

            #send it on discord
    await ctx.send(embed = e)

client.run(os.environ.get('Bot_Token'))