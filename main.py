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



        # print(next(resQ.results)["subpod"]["img"]["@src"])


@client.command()
async def mup(ctx):
    await ctx.send("Im ready.")

@client.command()
async def math(ctx, *, question):

            #initialized wolframalpha client with api token from .env file
    math = wolframalpha.Client(os.environ.get('Wolframaplha_API'))
            #query question from api and put it in resQ
    resQ = math.query(str(question))
    # print(next(resQ.title).text)
            #find the actual answer in text
    answer = next(resQ.results).text
    image_addy= "https://www.iconsdb.com/icons/preview/red/wolfram-alpha-xxl.png"
    e = discord.Embed(color=0x7289da, description = f"{answer}")
    e.set_footer(text= f'Requested by {ctx.author}' , icon_url=image_addy)
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

@client.event
async def on_message(message):
    await client.process_commands(message)
    if client.user == message.author:
        return
    if "<@!840905807717335040>" in message.content:
        content = message.content
        content = content.replace("<@!840905807717335040>", " ")
        math = wolframalpha.Client(os.environ.get('Wolframaplha_API'))
        resQ = math.query(str(content))

        try:
            # answer = next(resQ.results).text

            Answer_image = next(resQ.results)["subpod"]["img"]["@src"]
            image_addy = "https://www.iconsdb.com/icons/preview/red/wolfram-alpha-xxl.png"
            e = discord.Embed(color=0x7289da)
            e.set_image(url=Answer_image)
            e.set_footer(text=f'Requested by {message.author}', icon_url=image_addy)
            await message.channel.send(embed=e)
        except StopIteration:
            await message.channel.send("I have no answers for you. :( ")

client.run(os.environ.get('Bot_Token'))