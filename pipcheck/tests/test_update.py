# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mock

from nose.tools import eq_ as assert_equals

from pipcheck.pipcheck import Update, UNKNOWN


def test_update_class():
    update = Update('Package Name', 1.1, 2.2)
    assert_equals(update.name, 'Package Name')
    assert_equals(update.current_version, 1.1)
    assert_equals(update.new_version, 2.2)


def test_update_repr():
    update = Update('Package Name', 1.1, 2.2)
    assert_equals(str(repr(update)), 'Update Package Name (1.1 to 2.2)')


def test_update_str():
    update = Update('Package Name', 1.1, 2.2)
    assert_equals(str(str(update)), 'Update Package Name (1.1 to 2.2)')


def test_update_str_up_to_date():
    update = Update('Package Name', 1.1, 1.1)
    assert_equals(str(update), 'Update Package Name (up to date)')


def test_update_up_to_date_property():
    update = Update('Package Name', 1.1, 1.1)
    assert_equals(update.up_to_date, True)

