# -*- coding: utf8 -*-
import mock

from nose.tools import eq_ as assert_equals

from pipcheck.pipcheck import Update


def test_update_class():
    update = Update('Package Name', 1.1, 2.2)
    assert_equals(update.name, 'Package Name')
    assert_equals(update.current_version, 1.1)
    assert_equals(update.new_version, 2.2)


def test_update_repr():
    update = Update('Package Name', 1.1, 2.2)
    assert_equals(repr(update), u'<Update Package Name (1.1 to 2.2)>')


def test_update_str():
    update = Update('Package Name', 1.1, 2.2)
    assert_equals(str(update), u'Update Package Name (1.1 to 2.2)')

