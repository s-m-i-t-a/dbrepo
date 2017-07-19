# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, missing-docstring, invalid-name

import pytest

from pyresult import is_ok
from pyrsistent import PRecord, field

from dbrepo.repo import get_name
from dbrepo.fields import id_field


pytestmark = pytest.mark.usefixtures("db")


class TRecord(PRecord):
    _id = id_field()
    x = field()


def should_create_index(dtb, repo):
    rv = repo.index(TRecord, 'x')

    assert is_ok(rv)

    info = dtb.db[get_name(TRecord)].index_information()

    assert any([item['key'][0][0] == 'x' for item in info.values()])
