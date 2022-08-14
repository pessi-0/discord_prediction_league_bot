from replit import db
import aiohttp
import os
import re

async def get_players():
  async with aiohttp.ClientSession() as session:
    url = "https://v3.football.api-sports.io/players/squads"
    headers = {
      'x-rapidapi-host': "v3.football.api-sports.io",
      'x-rapidapi-key': os.getenv('API-KEY')
    }
    params = [('team', '529')]
    response = await session.get(url=url, params=params, headers=headers)
    body = await response.json(encoding='utf-8')
    players = body['response'][0]['players']
    db['players'] = {}
    for player in players:
      db['players'][player['name'].upper()] = {'id': player['id'], 'number': player['number']}
      db['alias'][player['name'].upper()] = player['name'].upper()

async def show_players(channel):
  x = 'Number Name'
  for p in db['players']:
    s = '\n{0:4s}   {1:30s}'.format(str(db['players'][p]['number']), p)
    x += s
  
  x = '```\n'+x+'\n```'
  await channel.send(x)

async def add_alias(message):
  match = re.match(r'^\$add-alias\s+"(.*)"\s+"(.*)"\s*$', message.content)
  if match is None:
    await message.channel.send('Please for the love of god use right format')
    return
  alias = match.group(1)
  alias = alias.upper()
  name = match.group(2)
  name = name.upper()
  # alias = ' '.join(x[1:-1])
  if name not in db['players']:
    await message.channel.send('Not a player of FC Barcelona')
  db['alias'][alias] = name
  show_str = 'Alias added: ' + alias + ' for ' + db['alias'][alias]
  await message.channel.send(show_str)

async def show_alias(message):
  x = message.content.strip().split(' ')
  alias = ' '.join(x[1:])
  alias = alias.upper()
  if alias not in db['alias']:
    await message.channel.send('No such alias')

  show_str = 'Alias: ' + alias + ' for ' + db['alias'][alias]
  await message.channel.send(show_str)

async def show_alias_all(channel):
  x = ['{0:30s} Name'.format('Alias')]
  i = 0
  alias_arr = []
  for alias in db['alias']:
    alias_arr.append((alias, db['alias'][alias]))
  alias_arr.sort(key=lambda t: t[1])
  for (alias, name) in alias_arr:
    if alias == name:
      continue
    str = '\n{0:30s} {1}'.format(alias, name)
    if not len(x[i]+str)<1990:
      i += 1
      x.append('{0:30s} Name'.format('Alias'))
    x[i] += str
  for x_t in x:
    x_t = '```\n'+x_t+'\n```'
    await channel.send(x_t)