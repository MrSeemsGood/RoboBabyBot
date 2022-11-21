import os
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

# hold ids of custom emojis and channels
SERVER_EMOTES = {
  'lok' : '<:rplus_lok:932633483153641492>',
  'thumbs_up' : '<:thumbs_up:918592797366440006>',
  'q' : '<:blind_question:1012462184703467623>'
}
CHANNEL_IDS = {
  'art-and-sprites':1006519189864980491,
  'questions' : 912287542253092895
} 

def get_author_name(message):
  if message.author.nick is None:
    return message.author.name
  else:
    return message.author.nick


class RoboBaby(commands.Bot):
  def __init__(self):
    intents = discord.Intents(messages=True, message_content=True, emojis=True, emojis_and_stickers=True)
    super().__init__(command_prefix="!", intents=intents)

    self.token = os.environ['BOT_TOKEN']
    self.names = ('robo-baby', 'robobaby', 'robo baby', 'robo')

  async def on_ready(self):
    print('Bot is alive, nickname is:', bot.user)

bot = RoboBaby()

@bot.command(aliases=['createpoll', 'makepoll', 'mkpoll'])
async def poll(ctx, question, *options : str):
    if len(options) == 0:
      await message.channel.send('❌ Try creating a poll again!')
    elif len(options) > 6:
      await message.channel.send('❌ No more than 6 options')
    else:
      try:
        await ctx.message.delete()
      except discord.errors.Forbidden:
        pass
        
      poll_message = "📌 New poll created by " + get_author_name(ctx.message) +' 📌 \nQuestion: ' + question
      for i in range(len(options)):
        poll_message += '\n' + number_emojis[i] + ': ' + options[i]

      msg = await ctx.send(poll_message)
      for i in range(len(options)):
        await msg.add_reaction(number_emojis[i])

@bot.command()
async def cat(ctx):
  await ctx.message.reply(
    '| /\\\_/\\\n| >^,^<\n|   / \\\n|   |\_|)\_/'
  )

@bot.command()
async def wiki(ctx):
  await ctx.send(
    "📜 Here's a link to mod's wiki:\n https://repentanceplusmod.fandom.com/wiki/Repentance%2B_Mod_Wiki",
    reference=ctx.message.reference,
    suppress_embeds=True
  )

@bot.command()
async def unlocks(ctx):
  await ctx.send(
    SERVER_EMOTES['q'] + " Want to know more about unlocks? Check the wiki!\n https://repentanceplusmod.fandom.com/wiki/Achievements",
    reference=ctx.message.reference,
    suppress_embeds=True
  )

number_emojis = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣')
rudes = ('you suck', 'ew', 'lame', 'stupid', 'dumb', 'u suck')
greetings = ('hello', 'hi', 'hey', 'yo')
mornings = ('gm', 'morning', 'good morning')
nights = ('gn', 'night', 'good night')
people = ('all', 'yall', "y'all", 'chat', 'people', 'everybody', 'everyone', 'guys', 'ngs')

image_ext = ['image/avif', 'image/jpeg', 'image/png', 'image/svg+xml']
def message_contains_image(message):
  return any([
    attachment.content_type in image_ext for attachment in message.attachments
  ])

def message_contains_any_keyword(message, keywords, at_start=False, at_end=False):
  if at_start:
    return any(message.startswith(kw) for kw in keywords)
  elif at_end:
    return any(message.endswith(kw) for kw in keywords)
  else:
    return any(' '+kw in message or kw+' ' in message or ','+kw in message or kw+',' in message for kw in keywords)

def message_adressed_to_everyone(message):
  return message_contains_any_keyword(message, people)

def message_addressed_to_me(message):
  return message_contains_any_keyword(message, bot.names)

@bot.event
async def on_message(message):
  await bot.tree.sync()
  if message.author == bot.user:
    return

  await bot.process_commands(message)
  said = message.content.lower()
  # only react to messages that have your name in them
  if message_addressed_to_me(said):
    # say hello to bot
    if message_contains_any_keyword(said, greetings, at_start=True):
      await message.channel.send('Hello ' + get_author_name(message) +
                                 ', you are epic! 😎')
      return

    if message_contains_any_keyword(said, rudes):
      # say mean things about him
      await message.channel.send('Rude 😭')
      return

  if message_adressed_to_everyone(said):
    if message_contains_any_keyword(said, mornings, at_start=True):
      await message.reply('Good morning! ☀️')
      return
    
    if message_contains_any_keyword(said, nights, at_start=True):
      await message.reply('Good night! 😴')
      return

  if message.channel.id == CHANNEL_IDS['art-and-sprites'] and message_contains_image(message):
    await message.create_thread(name='Dicuss this piece of art 🖌',
                                auto_archive_duration=60,
                                reason='new image has been posted.')
    await message.add_reaction(SERVER_EMOTES['thumbs_up'])



keep_alive()
try:
  bot.run(bot.token)
except discord.errors.HTTPException:
  print('Too many requests. Rebooting...')
  os.system('kill 1')
  bot.run(bot.token)

