# coding: utf-8
u"""Подсистема деперсонализации данных.

.. note::

   D15n --- сокращение от Depersonalization.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

from .utils import D15nManagerRegistry


default_app_config = __name__ + '.apps.AppConfig'


#: Реестр менеджеров деперсонализации.
#:
#: .. note::
#:
#:    Данный реестр должен заполняться из основной системы в зависимости от
#:    её потребностей в деперсонализации баз данных.
d15n_managers_registry = D15nManagerRegistry()
# -----------------------------------------------------------------------------
# Проверка наличия в окружении пакета psycopg2
# (вместо него должен быть psycopg2-binary).

try:
    get_distribution('psycopg2')
except DistributionNotFound:
    pass
else:  # pragma: no cover
    try:
        get_distribution('psycopg2-binary')
    except DistributionNotFound:
        raise EnvironmentError(
            '"psycopg2-binary" package is not installed. Remove "psycopg2"'
        )
    else:
        raise EnvironmentError(
            '"psycopg2" and "psycopg2-binary" packages are installed '
            'together. Remove "psycopg2" package.'
        )
# -----------------------------------------------------------------------------
