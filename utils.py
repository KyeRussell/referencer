# -*- coding: utf-8 -*-
from getpass import getpass


def prompt(message, allowed_responses=None, password=False):
    valid = False
    input_function = getpass if password else input
    while not valid:
        response = input_function('{}: '.format(message))
        if allowed_responses:
            response = response.lower()
            if response in allowed_responses:
                valid = True
        else:
            valid = True
    return response


def prompt_yes_no(message, default=True):
    # Build the prompt string
    if default is True:
        message = '{} [Y/n]'.format(message)
    else:
        message = '{} [y/N]'.format(message)
    response = prompt(message, allowed_responses=['yes', 'y', 'no', 'n', ''])
    if response == '':
        return default
    elif response in ['yes', 'y']:
        return True
    elif response in ['no', 'n']:
        return False
