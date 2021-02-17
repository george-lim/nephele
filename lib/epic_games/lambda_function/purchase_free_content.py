import epic_games_bot

from lib.core.dynamodb.users_table import UsersTable
from lib.core.interface import Interface
from lib.core.playwright import Playwright

def handler(event, _):
  interface = Interface(event['interface'])
  users_table = UsersTable(event['userId'])

  user = users_table.get_user()

  if not user.get('username') or not user.get('password'):
    interface.reply_message('Please log into Epic Games first.')
    raise Exception('missing account info')

  interface.reply_message('Purchasing free Epic Games content...')

  try:
    def bot(page):
      bot = epic_games_bot.EpicGamesBot(page, None, user['username'], user['password'])
      purchase_urls = bot.purchase_free_content()
      return purchase_urls

    playwright = Playwright(event['userId'])
    purchase_urls = playwright.execute(bot)

    if not purchase_urls:
      interface.reply_message('Already purchased free Epic Games content!')
    else:
      interface.reply_message('Successfully purchased free Epic Games content:')
      [interface.reply_message(purchase_url) for purchase_url in purchase_urls]
  except:
    screenshot_path = playwright.get_screenshot_path()

    if screenshot_path.exists():
      interface.reply_photo(screenshot_path)

    interface.reply_message('Failed to purchase free Epic Games content.')
    raise
