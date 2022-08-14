import aiohttp
import asyncio
import datetime as dt
import time
import players
from replit import db
import os

async def get_match(match_res):
  async with aiohttp.ClientSession() as session:
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
      'x-rapidapi-host': "v3.football.api-sports.io",
      'x-rapidapi-key': os.getenv('API-KEY')
    }
    date = dt.datetime.utcfromtimestamp(int(time.time())).strftime('%Y-%m-%d')
    params = [('team', '529'), ('season', '2022'), ('date', date)]
    # params = [('id', '869542')]
    response = await session.get(url=url, params=params, headers=headers)
    body = await response.json(encoding='utf-8')
    if not body['response']:
      params = [('team', '529'), ('season', '2022'), ('next', '1')]
      response = await session.get(url=url, params=params, headers=headers)
      body = await response.json(encoding='utf-8')
    db['match'] = body['response'][0]
    # print(db['match'])
    match_res.update(db['match']['fixture']['id'], db['match']['fixture']['timestamp'])

async def get_match_players_periodically(match_res):
  while True:
    await get_match(match_res)
    await players.get_players()
    midnight = dt.time(0,0,1,0)  
    now = int(time.time())
    now = dt.datetime.utcfromtimestamp(now)
    next_date = now.date()+dt.timedelta(days=1)
    next_midnight = dt.datetime.combine(next_date, midnight)
    tdelta = (next_midnight - now).total_seconds()
    await asyncio.sleep(tdelta)

async def print_curr_match(channel):
  show_str = db['match']['teams']['home']['name'] + ' vs ' + db['match']['teams']['away']['name'] + '\non ' + dt.datetime.utcfromtimestamp(db['match']['fixture']['timestamp']).strftime('%I:%M %p, %d %B, %Y') + ' (UTC)\nat ' + db['match']['fixture']['venue']['name'] + ',' + db['match']['fixture']['venue']['city']

  await channel.send(show_str)