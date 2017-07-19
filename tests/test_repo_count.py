# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, missing-docstring, invalid-name

import pytest

from pyresult import value
from pyrsistent import PRecord, field

from dbrepo.fields import id_field


pytestmark = pytest.mark.usefixtures("db")


class TRecord(PRecord):
    _id = id_field()
    text = field()


@pytest.fixture
def models(repo):

    records = (
        TRecord(text='Foo'),
        TRecord(text='Foo'),
        TRecord(text='Foo'),
        TRecord(text='Foo'),
        TRecord(text='Foo'),
        TRecord(text='Foo'),
        TRecord(text='Foo'),
        TRecord(text='Foo'),
        TRecord(text='Foo'),
        TRecord(text='Foo'),
    )

    return list(repo.create(test) for test in records)


def should_return_ok_result_with_count(models, repo):
    rv = repo.count(TRecord, filter={'text': 'Foo'})

    assert value(rv) == 10
