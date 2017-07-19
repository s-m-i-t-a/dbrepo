# -*- coding: utf-8 -*-

from pyrsistent import PClass, PRecord
from toolz import merge


def _get_projection_as_dict(projection):
    if isinstance(projection, dict):
        return projection

    return {key: True for key in projection}


def get_wanted_fields(schema):
    return {key: True for key in introspect(schema)['fields']}


def create_projection(schema, projection):
    return merge(
        _get_projection_as_dict(projection),
        get_wanted_fields(schema)
    )


def get_name(schema):
    return '%ss' % schema.__name__.lower()


def fqpn(klass):
    '''Return full import path

    :param klass: A class
    :return: full import path eg. 'foo.bar.Baz'
    '''
    return klass.__module__ + '.' + klass.__name__


def introspect(pclass_or_precord):
    '''Return info about precord/pclass fields

    Look at https://github.com/tobgu/pyrsistent/issues/47

    :param pclass_or_precord: PRecord/PClass class
    :return: info dict
    '''
    if issubclass(pclass_or_precord, PRecord):
        attr_name = "_precord_fields"
    elif issubclass(pclass_or_precord, PClass):
        attr_name = "_pclass_fields"
    else:
        return None

    record = {"fields": {}}

    for name, field_info in getattr(pclass_or_precord, attr_name).items():
        record[u"fields"][name] = sorted(
            fqpn(cls) for cls in field_info.type
        )

    return record
