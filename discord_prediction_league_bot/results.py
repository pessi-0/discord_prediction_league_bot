from replit import db
import asyncio
import aiohttp
import os
import time
import csv

def get_res(home, away):
  if home > away:
    return 1
  if home == away:
    return 0
  if home < away:
    return -1

async def print_stats(message):
  if str(message.author.id) not in db['results']:
    await message.channel.send('No stats for you yet')
    return
  show_str = message.author.name + '\'s stats:\n' + 'Played: ' + str(db['results'][str(message.author.id)]['played']) + '\nPoints: ' + str(db['results'][str(message.author.id)]['points']) + '\nResults guessed: ' + str(db['results'][str(message.author.id)]['results_guessed']) + '\nScores guessed: ' + str(db['results'][str(message.author.id)]['scores_guessed']) + '\nScorers guessed: ' + str(db['results'][str(message.author.id)]['scorers_guessed']) + '\nPPG: ' + str(db['results'][str(message.author.id)]['ppg'])

  await message.channel.send(show_str)

async def print_table(channel):
  if not db['results']:
    await channel.send('No results to show')
    return
  table = []
  for user in db['results']:
    table.append((db['results'][user]['name'], db['results'][user]['points'], db['results'][user]['ppg']))
  table.sort(reverse=True,key=(lambda x: x[2]))

  x = ['Rank {0:25s} Points PPG'.format('Name')]
  j = 0
  for (i,t) in enumerate(table):
    s = '\n{0:2d}   {1:25s} {2:6d} {3:0.2f}'.format(i, t[0], t[1], t[2])
    if not len(x[i]+s)<1990:
      j += 1
      x.append('Rank {0:25s} Points PPG'.format('Name'))
    x[j] += s

  # x = '```\n'+x+'\n```'
  for x_t in x:
    x_t = '```\n'+x_t+'\n```'
    await channel.send(x_t)
  # print(x)
  # await channel.send(x)

async def get_match_res(match_id):
  async with aiohttp.ClientSession() as session:
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
      'x-rapidapi-host': "v3.football.api-sports.io",
      'x-rapidapi-key': os.getenv('API-KEY')
    }
    params = [('id', str(match_id))]
    response = await session.get(url=url, params=params, headers=headers)
    body = await response.json(encoding='utf-8')
    match_res = body['response'][0]
    while match_res['fixture']['status']['short'] != 'FT':
      await asyncio.sleep(60)
      response = await session.get(url=url, params=params, headers=headers)
      body = await response.json(encoding='utf-8')
      match_res = body['response'][0]
    return match_res

async def calculate_results(match_id):
  print('calculatin!')
  match_res = await get_match_res(match_id)
  home = match_res['goals']['home']
  away = match_res['goals']['away']
  scorers = []
  for event in match_res['events']:
    if event['type'] == "Goal":
      if event['team']['id'] == 529:
        scorers.append(event['player']['id'])
  for user in db['predictions']:
    home_pred = db['predictions'][user]['home']
    away_pred = db['predictions'][user]['away']
    if home_pred == home and away_pred == away:
      db['results'][user]['points'] += 3
      db['results'][user]['scores_guessed'] += 1
      db['results'][user]['results_guessed'] += 1
    elif get_res(home, away) == get_res(home_pred, away_pred):
      db['results'][user]['points'] += 1
      db['results'][user]['results_guessed'] += 1
    scorers_pred = db['predictions'][user]['scorers']
    # print(db['results'][user]['points'])
    if scorers_pred and scorers:
      for s_pred in scorers_pred:
        flag = False
        for s in scorers:
          # print(scorers)
          s_pred = db['players'][db['alias'][s_pred]]['id']
          if s == s_pred:
            db['results'][user]['points'] += 1
            # print(db['results'][user]['points'])
            db['results'][user]['scorers_guessed'] += 1
            flag = True
            scorers.remove(s)
            break
        if not flag:
          # print('here')
          # db['results'][user]['points'] -= 1
          pass

    elif not scorers and scorers_pred:
      # db['results'][user]['points'] -= len(scorers_pred)
      pass
    db['results'][user]['ppg'] = db['results'][user]['points']/db['results'][user]['played']
  db['predictions'] = {}
  db['match'] = None
  with open('results.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Id', 'Name', 'Played', 'Points', 'Results guessed', 'Scores guessed', 'Scorers guessed', 'PPG'])
    for u in db['results']:
      writer.writerow([u, db['results'][u]['name'], db['results'][u]['played'], db['results'][u]['points'], db['results'][u]['results_guessed'], db['results'][u]['scores_guessed'], db['results'][u]['scorers_guessed'], db['results'][u]['ppg']])
  print('result calculated')

class Compute_result:
  def __init__(self):
    self._task = None
    self._done = False

  async def _job(self):
    await asyncio.sleep(self._timeout)
    await self._callback(self.match_id)
    self._done = True

  def cancel(self):
    self._task.cancel()

  def update(self, match_id, timestamp):    
    # if self.match_id == match_id and self.timestamp == timestamp:
    #   return
    print('updatin!')
    if self._task is not None:
      self.cancel()
    self.match_id = match_id
    self.timestamp = timestamp
    self._timeout = self.timestamp + 7200 - int(time.time())
    # self._timeout = 30
    self._callback = calculate_results
    self._task = asyncio.create_task(self._job())
    self._done = False
    