import shlex
import textnow_bot

from lib.core.dynamodb.users_table import UsersTable
from lib.core.interface import Interface
from lib.core.playwright import Playwright

def handler(event, _):
  interface = Interface(event['interface'])
  users_table = UsersTable(event['userId'])

  user = users_table.get_user()

  try:
    args = shlex.split(event['command'])[1:]
  except:
    interface.reply_message('Failed to parse input.')
    raise

  if len(args) < 2:
    interface.reply_message('Please provide a recipient and message to send.')
    raise Exception('missing recipient or message')

  if not user.get('cookies'):
    interface.reply_message('Please log into TextNow first.')
    raise Exception('missing login cookies')

  interface.reply_message('Sending TextNow message...')

  try:
    recipient = args[0]
    message = ' '.join(args[1:])

    def bot(page):
      bot = textnow_bot.TextNowBot(page, user['cookies'])
      bot.send_message(recipient, message)

    playwright = Playwright(event['userId'])
    playwright.execute(bot)

    interface.reply_message('Successfully sent TextNow message!')
  except:
    screenshot_path = playwright.get_screenshot_path()

    if screenshot_path.exists():
      interface.reply_photo(screenshot_path)

    interface.reply_message('Failed to send TextNow message.')
    raise
