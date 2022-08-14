async def show_help(channel):
  x = """
Welcome to General Young uns prediction league. The following commands will help you predict and track your results.
1. `$help`: show this message.
2. `$rules`: show rules of the competition.
3. `$match`: show the next Barcelona match (the bot updates every midnight so it may display outdated data sometime).
4. `$players`: show the players of Barcelona.
5. `$add-alias`: add an alias for the mentioned player. It is required so that you don't need to type the whole player name as stored in the database for making your prediction. To get the full player name, use `$players`.
Usage: `$add-alias "*alias*" "*full player name*"`
Example: `$add-alias "FdJ" "F. de Jong"`
6. `$show-alias`: Show if an alias exists or not.
Usage: `$show-alias *alias*`
Example: `$show-alias FdJ`
7. `$show-alias-all`: Show all aliases
8. `$predict`: add your prediction.
Usage: `$predict *home-score*-*away-score* [aliases of players you predict to score]`
Example: `$predict 2-0 [Auba, Frenkie]`
You can choose to not predict players too as follows: `$predict 2-0`
9. `$my-prediction`: show your prediction
10. `$stats`: show your stats so far
11. `$table`: show the current table of the competition"""
  await channel.send(x)

async def show_rules(channel):
  x = """
Rules of the prediction league are:
1. The point distribution is:
  +1 point for getting correct result
  +2 points for getting correct score
  +1 point for guessing correct scorer
  -1 point for guessing wrong scorer
  So for example you predict as follows: `$predict 2-0 [Auba, Frenkie]` and the result is 2-0 but Auba and Lewa score, you will get 3 points.
2. You can predict as many times as you want before the match starts.
3. To predict same player scoring multiple goals, you have to predict the player as many times
4. You can only predict Barcelona players for scorers
5. Please don't fuck around with the bot it hasn't been tested much
6. Please help add aliases for the players because if you use incorrect names the bot will not acept the prediction
7. Aliases are NOT case sensitive
  """
  await channel.send(x)