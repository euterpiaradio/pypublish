# coding=utf-8

options = dict()


def get_option(key):
    if key in options.keys():
        return options[key]
    else:
        raise AssertionError('options %s does not exist' % key)


def set_option(key, value):
    if key in options.keys():
        options[key] = value
    else:
        raise AssertionError('options %s does not exist' % key)
