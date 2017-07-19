# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,redefined-outer-name,invalid-name

import pytest

from pyresult import value
from pyrsistent import PRecord, field

from dbrepo.repo import get_name
from dbrepo.fields import id_field


pytestmark = pytest.mark.usefixtures("db")


class TRecord(PRecord):
    _id = id_field()
    x = field()


@pytest.fixture
def model():
    return TRecord(x=1)


@pytest.fixture
def collection(dtb):

    return dtb.db[get_name(TRecord)]


def should_save_record_to_dtb(collection, model, repo):
    repo.create(model)

    items = collection.find({'x': model.x})

    assert items.count() == 1

    item = items[0]

    assert item['x'] == model.x


def should_returns_status_ok_and_model_with_id(collection, model, repo):
    rv = repo.create(model)
    item = collection.find({'x': model.x})[0]

    assert value(rv)._id == str(item['_id'])  # pylint: disable=protected-access
