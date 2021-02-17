import shlex

from lib.core.interface import Interface
from lib.events.scheduler import Scheduler

def handler(event, _):
  interface = Interface(event['interface'])

  try:
    args = shlex.split(event['command'])[1:]
  except:
    interface.reply_message('Failed to parse input.')
    raise

  if len(args) < 3:
    interface.reply_message('Please provide a scheduled event name, cron expression, and command to put.')
    raise Exception('missing scheduled event info')

  try:
    [event_name, cron_expression, *command_args] = [*args]
    event['command'] = ' '.join(command_args)

    scheduler = Scheduler(event['userId'])
    scheduler.put_event(event_name, cron_expression, interface.get_request_arn(), event)

    interface.reply_message('Successfully put scheduled event!')
  except:
    interface.reply_message('Failed to put scheduled event: invalid event name or cron expression.')
    raise
