import epic_games_bot
import shlex

from lib.core.dynamodb.users_table import UsersTable
from lib.core.interface import Interface
from lib.core.playwright import Playwright

def handler(event, _):
  interface = Interface(event['interface'])

  try:
    args = shlex.split(event['command'])[1:]
  except:
    interface.reply_message('Failed to parse input.')
    raise

  if len(args) < 2:
    interface.reply_message('Please provide an account username and password to log into Epic Games.')
    raise Exception('missing account info')

  interface.reply_message('Logging into Epic Games...')

  try:
    user = { 'username': args[0], 'password': args[1] }

    bot = lambda page: epic_games_bot.EpicGamesBot(page, None, user['username'], user['password'])

    playwright = Playwright(event['userId'])
    playwright.execute(bot)

    users_table = UsersTable(event['userId'])
    users_table.update_user(user)

    interface.reply_message('Successfully logged into Epic Games!')
  except:
    screenshot_path = playwright.get_screenshot_path()

    if screenshot_path.exists():
      interface.reply_photo(screenshot_path)

    interface.reply_message('Failed to log into Epic Games: username and password combination may be invalid.')
    raise
