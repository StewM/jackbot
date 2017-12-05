# jackbot.py
# Main file for running the bot

import os, slackclient, time, pkgutil, random
from os.path import join, dirname
from dotenv import load_dotenv
import modules.commands
from modules.commands import *
from modules import helper
from modules import db

commands = []
for modname in pkgutil.iter_modules(modules.commands.__path__):
    commands.append(modname[1])

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

if os.environ.get('ENVIRONMENT'):
    if os.environ.get('ENVIRONMENT') == 'production':
        SLACK_NAME = os.environ.get('SLACK_NAME')
        SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
        SLACK_ID = os.environ.get('SLACK_ID')
    elif os.environ.get('ENVIRONMENT') == 'development':
        SLACK_NAME = os.environ.get('SLACK_DEV_NAME')
        SLACK_TOKEN = os.environ.get('SLACK_DEV_TOKEN')
        SLACK_ID = os.environ.get('SLACK_DEV_ID')
else:
    print('ERROR: Environment must be set for Bot to function.')
    exit()


SOCKET_DELAY = 1

# initialize db
db.create_logs_table()
# get bot's slack mention
slack_mention = helper.get_mention(SLACK_ID)


# run method
def run():
    # initialize slack client
    jackbot_slack_client = slackclient.SlackClient(SLACK_TOKEN)
    if jackbot_slack_client.rtm_connect():
        print(SLACK_NAME + ' Initialized.')
        while True:
            try:
                event_list = jackbot_slack_client.rtm_read()
            except (TimeoutError, AttributeError, BrokenPipeError) as e:
                print('Connection lost. Reconnecting. Reason: ' + e.__class__.__name__)
                event_list = []
                jackbot_slack_client = slackclient.SlackClient(SLACK_TOKEN)
                jackbot_slack_client.rtm_connect()
            except Exception as e:
                if e.__class__.__name__ == 'WebSocketConnectionClosedException':
                    print('Connection lost. Reconnecting. Reason: ' + e.__class__.__name__)
                    event_list = []
                    jackbot_slack_client = slackclient.SlackClient(SLACK_TOKEN)
                    jackbot_slack_client.rtm_connect()
                else:
                    raise
            if len(event_list) > 0:
                for event in event_list:
                    type = event.get('type')
                    # check if the event is a message
                    if type and type == 'message':
                        # get all the relevant parts of the event
                        text = event.get('text')
                        if text and isinstance(text, str):
                            user = event.get('user')
                            channel = event.get('channel')
                            # split the message into words
                            command_pieces = text.strip().split()
                            # check if first word is bot mention
                            if helper.is_command(command_pieces, user, SLACK_ID, slack_mention):
                                # handle command options
                                print(text)
                                helper.handle_command(jackbot_slack_client, command_pieces, text, user, channel, commands)
                            elif helper.is_mention(command_pieces, user, SLACK_ID, slack_mention):
                                # handle non-command mention
                                helper.handle_mention(jackbot_slack_client, command_pieces, text, user, channel)

            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')


if __name__ == '__main__':
    run()