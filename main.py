import os
import discord
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

intents = discord.Intents(0)
intents.messages = True
intents.message_content = True
intents.emojis = True
intents.emojis_and_stickers = True
client = discord.Client(intents=intents)
  
names = ('robo-baby', 'robobaby', 'robo baby', 'robo')
number_emojis = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣')
rudes = ('you suck', 'ew', 'lame', 'stupid', 'dumb', 'u suck')
greetings = ('hello', 'hi', 'hey', 'yo')
mornings = ('gm', 'morning', 'good morning')
nights = ('gn', 'night', 'good night')
people = ('all', 'yall', "y'all", 'chat', 'people', 'everybody', 'everyone', 'guys', 'ngs')

cat = '| /\\\_/\\\n| >^,^<\n|   / \\\n|   |\_|)\_/'

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
  return message_contains_any_keyword(message, names)

def get_author_name(message):
  if message.author.nick is None:
    return message.author.name
  else:
    return message.author.nick

# POLL EXAMPLE:
# [poll {t=Is turtle healthy to eat?}{yes}{no}{I am the turtle}]
def message_to_poll_options(message):
  c = message.content
  poll = '✅ Poll created by ' + get_author_name(message) + ':\n'
  if c.find('{t=') != -1:
    poll += 'Theme: ' + c[c.find('{t=') + 3:c.find('}')] + '\n'
    c = c[c.find('}') + 1:]
    
  num_options = 0
  while c.find('{') != -1:
    new_option = c[c.find('{') + 1:c.find('}')]
    poll += number_emojis[num_options] + ': ' + new_option + '\n'
    num_options += 1
    c = c[c.find('}') + 1:]

  return (poll, num_options)


@client.event
async def on_ready():
  print('Bot is alive, nickname is: {0.user}.'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

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

  if 'unlock' in said and message.channel.id == CHANNEL_IDS['questions']:
    link = await message.reply(
      SERVER_EMOTES['q'] + " Want to know more about unlocks? Check the wiki!\n https://repentanceplusmod.fandom.com/wiki/Achievements"
    )
    await link.edit(
      suppress=True
    )
    return

  if message_adressed_to_everyone(said):
    if message_contains_any_keyword(said, mornings, at_start=True):
      await message.reply('Good morning! ☀️')
      return
    
    if message_contains_any_keyword(said, nights, at_start=True):
      await message.reply('Good night! 😴')
      return

  # respond with wiki link
  if said == '[wiki]':
    link = await message.reply(
      "📜 Here's a link to mod's wiki:\n https://repentanceplusmod.fandom.com/wiki/Repentance%2B_Mod_Wiki")
    await link.edit(
      suppress=True
    )
    return

  if said == '[cat]':
    await message.reply(
      cat
    )
    return

  # create a poll
  if said.startswith('[poll ') and said.endswith('}]'):
    poll, num_options = message_to_poll_options(message)
    if num_options == 0:
      await message.channel.send('❌ Try creating a poll again!')
    elif num_options > 6:
      await message.channel.send('❌ No more than 6 options')
    else:
      try:
        await message.delete()
      except discord.errors.Forbidden:
        pass
      poll_message = await message.channel.send(poll)
      for i in range(num_options):
        await poll_message.add_reaction(number_emojis[i])

      return

  if message.channel.id == CHANNEL_IDS['art-and-sprites'] and message_contains_image(message):
    await message.create_thread(name='Dicuss this piece of art 🖌',
                                auto_archive_duration=60,
                                reason='new image has been posted.')
    await message.add_reaction(SERVER_EMOTES['thumbs_up'])



token = os.environ['BOT_TOKEN']
keep_alive()
try:
  client.run(token)
except discord.errors.HTTPException:
  print('Too many requests. Rebooting...')
  os.system('kill 1')
  client.run(token)
