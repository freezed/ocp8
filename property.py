#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-10-01
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

Train with properties
 """


class Adallas:
    """ training class """

    def __init__(self, param='La classe'):
        self._string = param

    def _get_value(self):
        mod_val = self._string.upper()
        return mod_val

    value = property(_get_value)

    def _get_extend_value(self):
        return '{} à Dallas'.format(self.value)

    extend = property(_get_extend_value)


def main():
    classadallas = Adallas()
    print(classadallas.extend)
    print(classadallas.value)
    print(classadallas.extend)


if __name__ == "__main__":
    main()
