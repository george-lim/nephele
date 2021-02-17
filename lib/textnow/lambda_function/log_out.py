from lib.core.dynamodb.users_table import UsersTable
from lib.core.interface import Interface

def handler(event, _):
  interface = Interface(event['interface'])
  users_table = UsersTable(event['userId'])

  try:
    users_table.update_user({})

    interface.reply_message('Successfully logged out of TextNow!')
  except:
    interface.reply_message('Failed to log out of TextNow.')
    raise
