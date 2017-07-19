# -*- coding: utf-8 -*-
'''Custom fields for pyrsistent PRecord'''

from pyrsistent import PSet, field, pset


def _field_no_invariant(_):
    '''
    Default NOOP invariant
    '''
    return (True, None)


def id_field():
    '''
    Return ID record id field
    '''
    return field(
        serializer=lambda _, value: str(value)
    )


def pset_field(initial=None, invariant=_field_no_invariant):
    '''
    Return set field

    :param initial: Initial value to pass to factory if no value is given for the field.
    :param mandatory: boolean specifying if the field is mandatory or not
    '''
    return field(
        type=PSet,
        initial=pset(initial),
        factory=pset,
        invariant=invariant,
        serializer=lambda _, val: list(val)
    )
