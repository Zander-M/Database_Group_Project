# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: May, 11, 2019
# Title: Factory Functions Test
"""
    tests for factory functions
"""

from AMS import create_app

def test_config():
    assert not create_app().testing
    assert create_app({"TESTING":True}).testing