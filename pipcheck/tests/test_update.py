# -*- coding: utf-8 -*-

#  Copyright 2014 Mike Jarrett
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

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

