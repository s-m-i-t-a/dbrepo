# -*- coding: utf-8 -*-

import pytest  # type: ignore

from pyrsistent import PRecord, pset

from dbrepo.fields import pset_field


def should_pset_have_init_values():
    init = [1, 2, 3, 4]

    class Test(PRecord):
        test = pset_field(initial=init)

    test = Test()

    assert test.test == pset(init)


def should_pset_field_call_invariant():
    data = [1, 2, 3, 4]

    def invariant(val):
        assert val == pset(data)

        return (True, None)

    class Test(PRecord):
        test = pset_field(invariant=invariant)

    test = Test(test=data)

    assert test.test == pset(data)

