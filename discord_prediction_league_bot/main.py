import discord
import os
from replit import db
import predictions
import matches
import results
import players
from keep_alive import keep_alive
import csv
import help

client = discord.Client()
db['predictions'] = {}
db['results'] = {}
db['match'] = None
db['players'] = {}
# db['alias'] = {}
current_match_res = results.Compute_result()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  # await players.get_players()
  try:
    with open('results.csv') as f:
      reader = csv.reader(f, delimiter=',')
      for row in reader:
        if row[0] == 'Id':
          continue
        db['results'][row[0]] = {'name': row[1], 'played': row[2], 'points': row[3], 'results_guessed': row[4], 'scores_guessed': row[5], 'scorers_guessed': row[6], 'ppg': row[7]}
  except:
    pass
  await matches.get_match_players_periodically(current_match_res)

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$help'):
    await help.show_help(message.channel)

  if message.content.startswith('$rules'):
    await help.show_rules(message.channel)

  if message.content.startswith('$predict'):
    await predictions.add_prediction(message)

  if message.content.startswith('$my-prediction'):
    await predictions.show_prediction(message)

  if message.content.startswith('$match'):
    await matches.print_curr_match(message.channel)

  if message.content.startswith('$stats'):
    await results.print_stats(message)

  if message.content.startswith('$table'):
    await results.print_table(message.channel)

  if message.content.startswith('$players'):
    await players.show_players(message.channel)

  if message.content.startswith('$add-alias'):
    await players.add_alias(message)

  if message.content.startswith('$show-alias-all'):
    await players.show_alias_all(message.channel)
  elif message.content.startswith('$show-alias'):
    await players.show_alias(message)

keep_alive()
client.run(os.getenv('TOKEN'))