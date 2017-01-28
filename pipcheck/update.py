# -*- coding: utf-8 -*-
from future.utils import python_2_unicode_compatible
from .constants import UNKNOWN


@python_2_unicode_compatible
class Update(object):

    @property
    def up_to_date(self):
        return self.current_version == self.new_version

    def __init__(self, name, current_version, new_version, prelease=False):
        self.name = name
        self.current_version = current_version
        self.new_version = new_version
        self.prelease = prelease

        if new_version == UNKNOWN:
            self.prelease = UNKNOWN  # pylint: disable=redefined-variable-type

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.current_version == other.current_version and
            self.new_version == other.new_version and
            self.prelease == other.prelease
        )

    def __str__(self):
        if self.up_to_date:
            return 'Update {name} (up to date)'.format(name=self.name)

        elif self.new_version == UNKNOWN:
            return 'Update {name} ({new_version})'.format(
                name=self.name,
                new_version=self.new_version
            )

        elif self.prelease:
            return (
                'Update {name} ({cur_ver} to {new_version} prelease)'.format(
                    name=self.name,
                    cur_ver=self.current_version,
                    new_version=self.new_version,
                )
            )
        else:
            return (
                'Update {name} ({current_version} to {new_version})'.format(
                    name=self.name,
                    current_version=self.current_version,
                    new_version=self.new_version,
                )
            )

    def __repr__(self):
        return str(self)
