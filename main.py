import os
import discord
from keep_alive import keep_alive

SERVER_EMOTES = {
  'lok' : '<:rplus_lok:932633483153641492>'
}
ART_AND_SPRITES_ID = 1006519189864980491

intents = discord.Intents(0)
intents.messages = True
intents.message_content = True
intents.emojis = True
intents.emojis_and_stickers = True
client = discord.Client(intents=intents)
  
names = ['robo-baby', 'robobaby', 'robo baby', 'robo']
greetings = ['hello', 'hi', 'hey', 'yo']
rudes = ['you suck', 'ew', 'lame', 'stupid', 'dumb', 'u suck']
mornings = ['gm', 'morning', 'good morning']
nights = ['gn', 'night', 'good night']
number_emojis = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣')

cat = '| /\\\_/\\\n| >^,^<\n|   / \\\n|   |\_|)\_/'

image_ext = ['image/avif', 'image/jpeg', 'image/png', 'image/svg+xml']
def message_contains_image(message):
  return any([
    attachment.content_type in image_ext for attachment in message.attachments
  ])


def get_author_name(message):
  if message.author.nick is None:
    return message.author.name
  else:
    return message.author.nick


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
  for name in names:
    # only react to messages that have your name in them
    if name in said:
      # say hello to bot
      for greeting in greetings:
        if said.startswith(greeting):
          await message.channel.send('Hello ' + get_author_name(message) +
                                     ', you are epic! 😎')
          return

      # say mean things about him
      for rude in rudes:
        if rude in said:
          await message.channel.send('Rude 😭')
          return

      for night in nights:
        if said.startswith(night):
          await message.reply('Good night! 😴')
          return

      for morning in mornings:
        if said.startswith(morning):
          await message.reply('Good morning! ☀️')
          return

    # respond with wiki link
    if said == '[wiki]':
      link = await message.reply(
        "📜 *here's a link to mod's wiki:* https://repentanceplusmod.fandom.com/wiki/Repentance%2B_Mod_Wiki"
      )
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

  if message.channel.id == ART_AND_SPRITES_ID and message_contains_image(message):
    await message.create_thread(name='Dicuss this piece of art 🖌',
                                auto_archive_duration=60,
                                reason='new image has been posted.')
    await message.add_reaction(SERVER_EMOTES['lok'])

token = os.environ['BOT_TOKEN']
keep_alive()
try:
  client.run(token)
except discord.errors.HTTPException:
  print('Too many requests. Rebooting...')
  os.system('kill 1')
  client.run(token)
