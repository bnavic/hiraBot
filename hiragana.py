import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="h!", intents=intents)

hiragana_dict = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
}

user_points = {}
current_hiragana = None
current_answer = None

@bot.command(name="hiragana")
async def hiragana_command(ctx):
    global current_hiragana, current_answer
    current_hiragana, current_answer = random.choice(list(hiragana_dict.items()))
    
    await ctx.send(f"Voici un hiragana : {current_hiragana} ! Quelle est sa prononciation ?")

@bot.event
async def on_message(message):
    global current_answer

    if message.author == bot.user:
        return

    if current_answer and message.content.lower() == current_answer:
        user_id = message.author.id

        if user_id in user_points:
            user_points[user_id] += 1
        else:
            user_points[user_id] = 1

        await message.channel.send(f"Bravo {message.author.mention} ! "
                                   f"Tu as trouvé la bonne réponse. "
                                   f"Tu as maintenant {user_points[user_id]} point(s) !")

        current_answer = None

    await bot.process_commands(message)

bot.run(token)
