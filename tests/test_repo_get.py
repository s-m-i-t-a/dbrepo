# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, missing-docstring, invalid-name

import pytest

from pyresult import value, is_error
from pyrsistent import PRecord, field

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
def model():
    return TRecord(x=1)


@pytest.fixture
def model2():
    return TRecord(x=2)


@pytest.fixture
def exmodel(dtb):
    model = ExtendedRecord(x=1, y=3)

    # save extended model to TRecord dtb, saving to own dtb not work
    dtb.db[get_name(TRecord)].insert_one(model.serialize())

    return model


@pytest.fixture
def save(dtb, model, model2):

    dtb.db[get_name(TRecord)].insert_one(model.serialize())
    dtb.db[get_name(TRecord)].insert_one(model2.serialize())

    return None


def should_return_selected_item(model, model2, save, repo):
    record = value(repo.get(TRecord, filter={'x': model.x}))
    record2 = value(repo.get(TRecord, filter={'x': model2.x}))

    assert record.x == model.x
    assert record2.x == model2.x


def should_return_error_when_nothing_found(repo):
    result = repo.get(TRecord, filter={'x': 2})

    assert is_error(result)
    assert result.value.message == 'Nothing found.'


def should_return_only_listed_fields(exmodel, repo):
    record = value(repo.get(TRecord, filter={'y': exmodel.y}))

    assert record.x == exmodel.x
