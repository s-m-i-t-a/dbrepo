# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, missing-docstring, too-many-arguments


from os.path import dirname, join

import pytest  # type: ignore

from pymongo import MongoClient


DB_CONFS = ('MONGO_URI', )


def connect(config):
    '''
    Connect to database
    '''
    dtbs = map(lambda s: MongoClient(config[s]).get_default_database(), DB_CONFS)
    return dtbs


def clean(dtb):
    '''
    Clean database
    '''
    for name in dtb.collection_names():
        if not name.startswith('system'):
            dtb.drop_collection(name)


# XXX: when object is created, call ensure_indexes,
# then indexes is set on recreated database.
# def ensure_indexes(sender, document, **kwargs):
#     document.ensure_indexes()


# signals.pre_init.connect(ensure_indexes)


TEST_LOG = join(dirname(dirname(__file__)), 'logs/tests.log')


class Db(object):
    def __init__(self, application):
        self.application = application

    def clean(self):
        # XXX: sice smaze vsechny data, ale pri tvorbe nove dtb uz nevytvori spravne indexy
        # smazeme vsechny vytvorene kolekce
        for dtb in connect(self.application.config):
            clean(dtb)


# @pytest.fixture
# def dtb():
#     return database


# @pytest.fixture
# def db(request, dtb):
#     db = Db(application=app)

#     request.addfinalizer(db.clean)

#     return db
