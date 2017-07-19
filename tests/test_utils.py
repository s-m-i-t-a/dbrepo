# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name

from pyrsistent import PRecord, field

from dbrepo.utils import create_projection, get_wanted_fields, get_name


class TRecord(PRecord):
    x = field()


def should_merge_projection_list():
    projection = ['a', 'b']

    rv = create_projection(TRecord, projection)

    for key, value in rv.items():
        assert key in ['a', 'b', 'x']
        assert value


def should_merge_projection_dict():
    projection = {
        'a': True,
        'b': True,
        'x': False,
    }

    rv = create_projection(TRecord, projection)

    for key, value in rv.items():
        assert key in ['a', 'b', 'x']
        assert value


def should_return_record_fields_as_projection_dict():
    rv = get_wanted_fields(TRecord)

    assert rv == {'x': True}
