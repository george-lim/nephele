import shlex
import textnow_bot

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
    interface.reply_message('Please provide an account username and password to log into TextNow.')
    raise Exception('missing account info')

  interface.reply_message('Logging into TextNow...')

  try:
    [username, password] = [*args]

    def bot(page):
      bot = textnow_bot.TextNowBot(page, None, username, password)
      return bot.get_cookies()

    playwright = Playwright(event['userId'])
    cookies = playwright.execute(bot)

    user = { 'cookies': cookies }

    users_table = UsersTable(event['userId'])
    users_table.update_user(user)

    interface.reply_message('Successfully logged into TextNow!')
  except:
    screenshot_path = playwright.get_screenshot_path()

    if screenshot_path.exists():
      interface.reply_photo(screenshot_path)

    interface.reply_message('Failed to log into TextNow: username and password combination may be invalid.')
    raise
