from src.common.actions import reply_message

def handler(event, context):
  reply_message(event['interface'], event['message'], parse_mode=event.get('parseMode'))
