from replit import db
import re
import time

prediction_regex = re.compile(r'^\$predict\s+(\d+\s*-\s*\d+)(\s+\[((.)+,)*(.)+\])?\s*$')

async def add_prediction(message):

  if db['match'] is None:
    await message.channel.send('No match to predict')
    return
  
  if int(time.time()) > db['match']['fixture']['timestamp']:
    await message.channel.send('Time to predict is over motherfucker')
    return

  match = prediction_regex.match(message.content)
  if match is None:
    await message.channel.send('Stop fucking with the bot with a wrong format')
    return

  score_pred = match.group(1)
  score_pred = score_pred.strip()
  [home, away] = score_pred.split('-')
  [home, away] = [int(home), int(away)]
  
  scorers = match.group(2)
  if scorers is not None:
    scorers = scorers.strip()
    scorers = scorers[1:-1]
    scorers = scorers.split(',')
    scorers = [p.strip().upper() for p in scorers]
  else:
    scorers = []

  for s in scorers:
    if s not in db['alias']:
      await message.channel.send(s + ': no such alias created')
      return

  num_s = len(scorers)
  if db['match']['teams']['home']['id'] == 529:
    if num_s > home:
      await message.channel.send('Can\'t have more scorers than goals twat')
      return
  else:
    if num_s > away:
      await message.channel.send('Can\'t have more scorers than goals twat')
      return
      

  # prev_pred = next((item for item in db['predictions'] if item['user']==message.author.id), None)
  # if prev_pred is not None:
  #   db['predictions'].remove(prev_pred)

  db['predictions'][str(message.author.id)] = {'home': home, 'away': away, 'scorers': scorers}
  if not str(message.author.id) in db['results']:
    db['results'][str(message.author.id)] = {'played':0, 'points':0, 'scores_guessed': 0, 'results_guessed': 0, 'scorers_guessed': 0, 'ppg': 0}

  db['results'][str(message.author.id)]['played'] += 1
  db['results'][str(message.author.id)]['name'] = message.author.name

  show_str = message.author.name + ' has predicted:\nScore: ' + db['match']['teams']['home']['name'] + ' ' + str(home) + '-' + str(away) + ' ' + db['match']['teams']['away']['name'] + '\nScorers: ' + str(scorers)

  await message.channel.send(show_str)

async def show_prediction(message):
  if str(message.author.id) not in db['predictions']:
    await message.channel.send('You have no current predictions')
    return
    
  home = db['predictions'][str(message.author.id)]['home']
  away = db['predictions'][str(message.author.id)]['away']
  scorers = db['predictions'][str(message.author.id)]['scorers']
  scorers = list(scorers)
  show_str = 'You have predicted:\nScore: ' + db['match']['teams']['home']['name'] + ' ' + str(home) + '-' + str(away) + ' ' + db['match']['teams']['away']['name'] + '\nScorers: ' + str(scorers)

  await message.channel.send(show_str)
