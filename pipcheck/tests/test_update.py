# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from pipcheck.pipcheck import Update


class TestUpdate(TestCase):

    def test_update_class(self):
        update = Update('Package Name', 1.1, 2.2)
        self.assertEqual(update.name, 'Package Name')
        self.assertEqual(update.current_version, 1.1)
        self.assertEqual(update.new_version, 2.2)

    def test_update_repr(self):
        update = Update('Package Name', 1.1, 2.2)
        self.assertEqual(str(repr(update)), 'Update Package Name (1.1 to 2.2)')

    def test_update_str(self):
        update = Update('Package Name', 1.1, 2.2)
        self.assertEqual(str(str(update)), 'Update Package Name (1.1 to 2.2)')

    def test_update_str_up_to_date(self):
        update = Update('Package Name', 1.1, 1.1)
        self.assertEqual(str(update), 'Update Package Name (up to date)')

    def test_update_up_to_date_property(self):
        update = Update('Package Name', 1.1, 1.1)
        self.assertEqual(update.up_to_date, True)
