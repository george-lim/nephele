from lib.core.interface import Interface
from lib.events.scheduler import Scheduler

def handler(event, _):
  interface = Interface(event['interface'])

  try:
    scheduler = Scheduler(event['userId'])
    events = scheduler.list_events()

    if not events:
      interface.reply_message('No scheduled events found!')
    else:
      for event in events:
        interface.reply_message(f'''Name: {event['name']}
State: {event['state']}
Cron Expression: {event['cron_expression']}
Command: {event['command']}''')
  except:
    interface.reply_message('Failed to list scheduled events.')
    raise
