from lib.core.interface import Interface

def handler(event, _):
  interface = Interface(event['interface'])
  interface.reply_message(event['message'], event.get('parseMode'))
