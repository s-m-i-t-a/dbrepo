# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name, redefined-outer-name

from random import randint

import pytest

from pyresult import value, rmap
from pyrsistent import PRecord, field
from toolz import pipe

from dbrepo.repo import get_name
from dbrepo.fields import id_field


pytestmark = pytest.mark.usefixtures("db")


class TRecord(PRecord):
    _id = id_field()
    x = field()


class ExtendedRecord(PRecord):
    _id = id_field()
    x = field()
    y = field()


@pytest.fixture
def models(dtb):

    models = [TRecord(x=i) for i in range(randint(10, 100))]

    for model in models:
        dtb.db[get_name(TRecord)].insert_one(model.serialize())

    return models


@pytest.fixture
def exmodels(dtb):
    models = [ExtendedRecord(x=i, y=i * 10) for i in range(randint(10, 100))]

    for model in models:
        # save extended model to TRecord dtb, saving to own dtb not work
        dtb.db[get_name(TRecord)].insert_one(model.serialize())

    return models


def should_return_all_items_in_db(models, repo):
    records = [TRecord(x=r.x) for r in value(repo.all(TRecord))]

    assert len(records) == len(models)

    for record in records:
        assert record in models


def should_return_all_items_in_db_with_only_listed_fields(exmodels, repo):
    records = pipe(
        repo.all(TRecord),
        rmap(list),  # pylint: disable=no-value-for-parameter
        value
    )

    assert len(records) == len(exmodels)
    xs = [item.x for item in exmodels]

    for record in records:
        assert record.x in xs
