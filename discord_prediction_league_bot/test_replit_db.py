# from replit import db
# import predictions
# import matches
# import results
# import players
# import asyncio

# # db['predictions'] = []

# print(db['match'])
# db['test'] = []
# print(db['test'])
# if not db['test']:
#   print(True)

# db['predictions'] = {}
# db['results'] = {}
# db['match'] = None
# db['players'] = {}
# db['alias'] = {}
# db['alias']['Dembele'] = 'O. Dembélé'
# db['predictions']['1'] = {'home': 2, 'away': 2, 'scorers': ['Dembele', 'Dembele']}
# db['results_t'] = {'-1': {}}
# print(db['results_t']['-1'])
# # db['results']['1']['name'] = 'Pessi'
# db['results_t']['-1'] = {'name': 'Pessi', 'played':1, 'points':0, 'scores_guessed': 0, 'results_guessed': 0, 'scorers_guessed': 0}
# current_match_res = results.Compute_result()

# async def main():
#   await players.get_players()
#   await matches.get_match(current_match_res)
#   await asyncio.sleep(35)
#   # await players.show_alias_all(1)

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.run_until_complete(loop.shutdown_asyncgens())
#     loop.close()

# # print(db['predictions'])
# # print(db['results'])
# # print(db['alias'])
# # print(db['players'])

# # import time
# # import datetime as dt

# # date = dt.datetime.utcfromtimestamp(int(time.time())).strftime('%Y-%m-%d')
# # print(date)
# # print(db.keys())
# # del db["test"]
# # print(players.show_alias_all(1))