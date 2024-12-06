# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields import TextField
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.db.utils import ProgrammingError

from .constants import CORE_SCHEMA


class ReadOnlyQuerySet(QuerySet):

    """QuerySet, предотвращающий изменение данных в модели."""

    # pylint: disable=arguments-differ

    @property
    def __exception(self):
        return ProgrammingError(
            '{} is read only.'.format(self.__class__.__name__)
        )

    def create(self, *args, **kwargs):
        """Запрещает создание записей.

        :raises: ProgrammingError: при каждом вызове.
        """
        raise self.__exception

    def bulk_create(self, *args, **kwargs):
        """Запрещает массовое создание записей.

        :raises: ProgrammingError: при каждом вызове.
        """
        raise self.__exception

    def select_for_update(self, *args, **kwargs):
        """Запрещает выбор записей для последующего изменения.

        :raises: ProgrammingError: при каждом вызове.
        """
        raise self.__exception

    def update(self, *args, **kwargs):
        """Запрещает изменение записей.

        :raises: ProgrammingError: при каждом вызове.
        """
        raise self.__exception

    def update_or_create(self, *args, **kwargs):
        """Запрещает создание или изменение записей.

        :raises: ProgrammingError: при каждом вызове.
        """
        raise self.__exception

    def delete(self, *args, **kwargs):
        """Запрещает удаление записей.

        :raises: ProgrammingError: при каждом вызове.
        """
        raise self.__exception


class ReadOnlyManager(BaseManager.from_queryset(ReadOnlyQuerySet)):

    """Менеджер моделей для режима "только для чтения"."""

    use_for_related_fields = True


class FieldConfig(Model):

    """Параметры деперсонализации поля.

    .. tip::

       В случае, если деперсонализация включена не только в БД по умолчанию,
       рекомендуется использовать метод :meth:`~django.db.models.query.
       QuerySet.using` для выбора БД.

    .. attention::

       Данная модель доступна в режиме только для чтения. При попытке изменения
       данных в ней будет исключение :class:`~django.db.ProgrammingError`.
    """

    table_schema = CharField(
        'Имя схемы',
        max_length=64,
    )
    table_name = CharField(
        'Имя таблицы',
        max_length=64,
    )
    column_name = CharField(
        'Имя поля',
        max_length=64,
    )
    function_schema = CharField(
        'Имя деперсонализирующей функции',
        max_length=64,
    )
    function_name = CharField(
        'Имя деперсонализирующей функции',
        max_length=64,
    )
    function_params = TextField(
        'Параметры деперсонализирующей функции',
    )

    class Meta:  # noqa: D106
        verbose_name = 'Параметры деперсонализации поля'
        verbose_name_plural = 'Параметры деперсонализации БД'

        db_table = '{schema_name}"."{table_name}'.format(
            schema_name=CORE_SCHEMA,
            table_name='columns_config_as_names',
        )
        managed = False

    def __repr__(self):
        return '{}<{}.{}({}.{}.{}{})>'.format(
            self.__class__.__name__,
            self.function_schema,
            self.function_name,
            self.table_schema,
            self.table_name,
            self.column_name,
            ', ' + self.function_params if self.function_params else '',
        )
    # -------------------------------------------------------------------------
    # Реализация режима только для чтения.

    objects = ReadOnlyManager()

    @property
    def __exception(self):
        return ProgrammingError(
            '{} is read only.'.format(self.__class__.__name__)
        )

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Запрещает сохранение объектов модели."""
        raise self.__exception

    def delete(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Запрещает удаление объектов модели."""
        raise self.__exception
    # -------------------------------------------------------------------------
