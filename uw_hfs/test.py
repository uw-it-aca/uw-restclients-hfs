# This is just a test runner for coverage
from commonconf.backends import use_configparser_backend
from os.path import abspath, dirname
import os

if __name__ == '__main__':
    from nose2 import discover
    discover()
