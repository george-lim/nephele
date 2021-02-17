import kijiji_bot
import shlex

from lib.core.dynamodb.users_table import UsersTable
from lib.core.interface import Interface

def handler(event, _):
  interface = Interface(event['interface'])

  try:
    args = shlex.split(event['command'])[1:]
  except:
    interface.reply_message('Failed to parse input.')
    raise

  if len(args) < 1:
    interface.reply_message(
      '''Please provide a SSID cookie value to log into Kijiji\. To get this value:

1\. Log into Kijiji on a browser, with `Keep me signed in` checked
2\. Using a web inspector, copy the value of the `ssid` cookie in the domain `www\.kijiji\.ca`

Ensure that you do not log out of the Kijiji session afterwards\. If you do, you will need another SSID to authenticate again\.''',
      parse_mode='MarkdownV2'
    )

    raise Exception('missing ssid')

  interface.reply_message('Logging into Kijiji...')

  try:
    user = { 'ssid': args[0] }

    kijiji_bot.KijijiBot(user['ssid'])

    users_table = UsersTable(event['userId'])
    users_table.update_user(user)

    interface.reply_message('Successfully logged into Kijiji!')
  except:
    interface.reply_message('Failed to log into Kijiji: invalid SSID.')
    raise
