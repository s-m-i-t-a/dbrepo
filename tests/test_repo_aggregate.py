# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, missing-docstring, invalid-name

from collections import OrderedDict

import pytest

from pyresult import value
from pyrsistent import PRecord

from dbrepo.fields import id_field, pset_field


pytestmark = pytest.mark.usefixtures("db")


class TRecord(PRecord):
    _id = id_field()
    tags = pset_field()


@pytest.fixture
def models(repo):

    records = (
        TRecord(tags=['foo']),
        TRecord(tags=['foo', 'bar']),
        TRecord(tags=['foo', 'bar', 'baz']),
    )

    return list(repo.create(test) for test in records)


def should_return_aggregated_result(models, repo):
    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": OrderedDict([("count", -1), ("_id", -1)])}
    ]

    result = {res['_id']: res['count'] for res in value(repo.aggregate(TRecord, pipeline=pipeline))}

    assert result['foo'] == 3
    assert result['bar'] == 2
    assert result['baz'] == 1
