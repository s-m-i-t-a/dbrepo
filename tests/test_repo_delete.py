# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, missing-docstring, invalid-name

import pytest

from bson.objectid import ObjectId
from pyresult import value, is_ok
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


def should_remove_item_from_dtb(collection, model, repo):
    saved_model = value(repo.create(model))

    repo.delete(TRecord, filter={'_id': ObjectId(saved_model._id)})

    items = collection.find({'_id': ObjectId(saved_model._id)})

    assert items.count() == 0


def should_remove_all_items_corresponding_to_the_query(collection, model, repo):
    for _ in range(10):
        repo.create(model)

    items = collection.find({'x': model.x})

    assert items.count() == 10

    rv = repo.delete(TRecord, filter={'x': model.x})
    assert is_ok(rv)

    items = collection.find({'x': model.x})

    assert items.count() == 0
