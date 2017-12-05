import random
from datetime import date, datetime
import modules.commands
from modules.commands import *
from modules import db


def get_mention(user):
    return '<@{user}>'.format(user=user)


def deny_request(user_mention):
    response_template = "I'm sorry, {mention}. I'm afraid I can't do that."
    return response_template.format(mention=user_mention)


def check_list_in_list(needles, haystack):
    for needle in needles:
        if needle.lower() in haystack:
            return True

    return False


def post_message(jackbot_slack_client, message, channel):
    jackbot_slack_client.api_call('chat.postMessage', channel=channel, text=message, as_user=True)


def is_command(command_pieces, user, SLACK_ID, slack_mention):
    # Check if this is a command
    # check if not my own event
    if not(user == SLACK_ID):
        # in case it is not a private message check mention
        if len(command_pieces) > 0:
            first = command_pieces[0]
        else:
            first = ''
        if first == slack_mention:
            return True


def is_mention(command_pieces, user, SLACK_ID, slack_mention):
    # check if this message mentions me
    if not(user == SLACK_ID):
        if slack_mention in command_pieces:
            return True


def handle_command(jackbot_slack_client, command_pieces, text, user, channel, commands):
    if len(command_pieces) > 1:
        command = command_pieces[1].lower()
    else:
        command = ''

    if command in commands:
        status = getattr(modules.commands, command).handle(jackbot_slack_client, command_pieces, text, user, channel)
        db.log_event(user, text, datetime.now(), status)
    else:
        post_help(jackbot_slack_client, command_pieces, channel)


def handle_mention(jackbot_slack_client, command_pieces, text, user, channel):
    thanks = ['thanks', 'thank', 'thankyou']
    hellos = ['hi', 'hello', 'greetings', 'hey']

    yw_messages = ["No problem!", "You're welcome!", "It's the least I could do.", "Glad I could help!"]
    hi_messages = ["Hello!", "Hi!", "Hi, how are you?", "Hello! Hope you're having a nice day!", "Hi. Let me know if you need to deploy."]

    if check_list_in_list(needles=command_pieces, haystack=hellos):
        # send hello
        message = random.choice(hi_messages)
        post_message(jackbot_slack_client, message, channel)
    elif check_list_in_list(needles=command_pieces, haystack=thanks):
        # send thanks
        message = random.choice(yw_messages)
        post_message(jackbot_slack_client, message, channel)


def post_help(jackbot_slack_client, command_pieces, channel, commands, SLACK_NAME):
    if len(command_pieces) > 2:
        if command_pieces[2].lower() in commands and command_pieces[1].lower() == 'help':
            arg = command_pieces[2].lower()
        else:
            arg = ''
    else:
        arg = ''

    if arg == '':
        message = "Available Commands:\n"
        for command in commands:
            message += command + " : " + getattr(modules.commands, command).get_help(simple=True) + "\n"
        message += "If specific command help is needed type _@" + SLACK_NAME + " help {command}_"
        post_message(jackbot_slack_client=jackbot_slack_client, message=message, channel=channel)
    else:
        message = getattr(modules.commands, arg).get_help(simple=False)
        post_message(jackbot_slack_client=jackbot_slack_client, message=message, channel=channel)
