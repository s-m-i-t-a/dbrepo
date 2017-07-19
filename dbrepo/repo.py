# -*- coding: utf-8 -*-
# pylint: disable=no-value-for-parameter

import logging

from pymongo.errors import PyMongoError
from pyresult import (
    ok,
    error,
    rmap,
    and_then,
    from_try_except
)
from toolz import pipe

from dbrepo.utils import get_name, create_projection


LOG = logging.getLogger('dbrepo')


class Repo(object):
    def __init__(self, db):
        self.db = db

    def all(self, schema, **kwargs):
        '''Find all objects in dtb'''
        kwargs['projection'] = create_projection(schema, kwargs.get('projection', {}))

        return pipe(
            from_try_except(self.db.db[get_name(schema)].find, **kwargs),
            rmap(lambda q: map(schema.create, q))
        )

    def create(self, record):
        '''Save record to dtb.'''
        try:
            return pipe(
                self.db.db[get_name(type(record))].insert_one(record.serialize()),
                ok,
                rmap(lambda result: str(result.inserted_id)),
                rmap(lambda id_: record.set(_id=id_))
            )
        except PyMongoError as err:
            return error(err)

    def index(self, schema, keys, **kwargs):
        '''Create index on selected schema'''
        LOG.debug('Creating index for \'%s\' with keys \'%s\' and extras \'%s\'', schema, keys, kwargs)
        try:
            return ok(self.db.db[get_name(schema)].create_index(keys, **kwargs))
        except PyMongoError as err:
            return error(err)

    def get(self, schema, **kwargs):
        '''Get record from dtb.'''
        kwargs['projection'] = create_projection(schema, kwargs.get('projection', {}))
        return pipe(
            from_try_except(self.db.db[get_name(schema)].find_one, **kwargs),
            and_then(
                lambda r: ok(schema.create(r))
                if r is not None else error('Nothing found.'),
            )
        )

    def aggregate(self, schema, **kwargs):
        ''' Return aggregate result on selected schema
        '''
        try:
            return ok(self.db.db[get_name(schema)].aggregate(**kwargs))
        except PyMongoError as err:
            return error(err)

    def delete(self, schema, **kwargs):
        '''Remove item from dtb and return result'''
        try:
            return ok(self.db.db[get_name(schema)].delete_many(**kwargs))
        except PyMongoError as err:
            return error(err)

    def count(self, schema, **kwargs):
        '''Return count of items in result'''
        return pipe(
            from_try_except(self.db.db[get_name(schema)].count, **kwargs),
        )
