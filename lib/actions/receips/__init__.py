import importlib


def find_receipt(name):
    return importlib.import_module("%s.%s" % (__name__, name))
