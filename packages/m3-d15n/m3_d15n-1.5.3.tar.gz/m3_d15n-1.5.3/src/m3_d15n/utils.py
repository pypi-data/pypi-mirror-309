# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import defaultdict
from importlib import import_module
from itertools import groupby
from operator import itemgetter
from os.path import dirname
from os.path import join
import codecs
import contextlib

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connections
from django.db import router
from django.db.backends.signals import connection_created
from django.db.models.signals import post_migrate
from django.db.models.signals import pre_migrate
from django.db.transaction import atomic
from django.db.utils import ProgrammingError
from django.utils.functional import cached_property
from psycopg2.extensions import QuotedString
from psycopg2.extensions import quote_ident
from six import PY2
from six import iteritems
from six import itervalues
from six import string_types
from six import text_type
from six.moves.collections_abc import Iterable

from ._external_utils import Lock
from ._external_utils import is_in_migration_command
from .constants import CORE_SCHEMA
from .constants import DATA_SCHEMA
from .signals import post_add_field
from .signals import post_delete_field
from .signals import post_install
from .signals import post_switch_mode
from .signals import post_uninstall
from .signals import pre_add_field
from .signals import pre_delete_field
from .signals import pre_install
from .signals import pre_switch_mode
from .signals import pre_uninstall


# -----------------------------------------------------------------------------
# Внутренние вспомогательные инструменты.


class _SuspendConfigTriggers(object):

    def __init__(self, connection):
        self._connection = connection

    _sql = """
        alter table {core_schema}.columns_config
        {{action}} trigger {core_schema}_{{name}}
    """.format(core_schema=CORE_SCHEMA)

    def __enter__(self):
        with contextlib.closing(self._connection.cursor()) as cursor:
            cursor.execute(self._sql.format(
                action='disable',
                name='columns_config_changed',
            ))

    def __exit__(self, exc_type, exc_val, exc_tb):
        with contextlib.closing(self._connection.cursor()) as cursor:
            cursor.execute(self._sql.format(
                action='enable',
                name='columns_config_changed',
            ))


class _ConnectionMixin(object):

    """Класс-примесь для работы с подключением к БД."""

    def __init__(self, database_alias, *args, **kwargs):
        """Инициализация экземпляра класса.

        :param str database_alias: Алиас деперсонализируемой базы
            данных.
        """
        super(_ConnectionMixin, self).__init__(*args, **kwargs)

        self.alias = database_alias

        if self._connection.vendor != 'postgresql':  # pragma: no cover
            raise ImproperlyConfigured(
                'Деперсонализация поддерживается только для СУБД PostgreSQL'
            )

    @property
    def _connection(self):
        """Подключение к базе данных.

        :rtype: django.db.backends.postgresql.base.DatabaseWrapper
        """
        result = connections[self.alias]
        return result

    @property
    def _cursor(self):
        """Курсор для выполнения запросов к БД.

        :rtype: django.db.backends.utils.CursorWrapper
        """
        result = self._connection.cursor()
        return result

    @cached_property
    def _dbname(self):
        """Имя базы данных.

        :rtype: str
        """
        return self._connection.get_connection_params()['database']


def _is_initialized(database_alias):
    """Возвращает True, если представление для FieldConfig есть в БД.

    :rtype: bool
    """
    with connections[database_alias].cursor() as cursor:
        cursor.execute("""
            select
                1
            from
                pg_class tables
                inner join pg_catalog.pg_namespace schemas on (
                    tables.relnamespace = schemas.oid
                )
            where
                tables.relkind = 'v' and
                schemas.nspname = '{core_schema}' and
                tables.relname = 'columns_config_as_names'
        """.format(
            core_schema=CORE_SCHEMA,
        ))
        result = cursor.fetchone() is not None

    return result
# -----------------------------------------------------------------------------


class ParamsManager(_ConnectionMixin):

    """Менеджер параметров подсистемы деперсонализации.

    Обеспечивает чтение и установку значений параметров в БД.

    .. automethod:: __init__
    """

    #: Значения некоторых параметров по умолчанию.
    defaults = dict(
        visible_chars_begin=2,
        visible_chars_end=0,
        result_length=10,
        fill_char='*',
    )

    def __init__(self, database_alias, defaults=None):
        """Инициализация класса.

        :param basestring database_alias: Алиас деперсонализируемой базы
            данных.
        :param dict defaults: Словарь со значениями параметров по умолчанию.
            Если не указан, то используется :attr:`defaults`.
        """
        super(ParamsManager, self).__init__(database_alias)

        if defaults:  # pragma: no cover
            self.defaults = defaults
        else:
            self.defaults = ParamsManager.defaults.copy()

        connection_created.connect(
            self._on_connection_created,
            dispatch_uid='m3_d15n.DatabaseParams.connection_created'
        )

    def _on_connection_created(self, connection, **kwargs):
        """При подключении устанавливает параметры подсистемы в БД.

        Т.к. параметры, установленные с помощью функции ``set_config``
        действуюют только в рамках текущего сеанса, необходимо при каждом
        подключении заново устанавливать значения всех параметров.
        """
        if connection.alias == self.alias:
            for param_name, param_value in iteritems(self.defaults):
                setattr(self, param_name, param_value)

    def _get_param(self, name, default_value=None):
        """Вызывает функцию ``current_setting`` в БД.

        :param base_string name: имя параметра.
        :param basestring default: значение параметра по умолчанию.
        """
        with self._cursor as cursor:
            try:
                cursor.callproc(CORE_SCHEMA + '.get_param', (name,))
            except ProgrammingError:  # pragma: no cover
                result = default_value
            else:
                result = cursor.fetchone()[0]

        return result

    def _set_session_param(self, name, value):
        """Устанавливает значение параметра в текущем подключении к БД.

        :param str name: имя параметра (должно содержать точку, т.к. параметры
            без точки считаются системными параметрами PostgreSQL).
        :param str value: значение параметра.
        """
        assert '.' in name, name

        with self._cursor as cursor:
            cursor.callproc('set_config', (name, text_type(value), False))

    @property
    def visible_chars_begin(self):
        """Количество видимых символов в начале строки.

        Параметр используется функцией деперсонализации ``depersonalize_name``.

        :rtype: int
        """
        result = max(0, int(
            self._get_param(
                CORE_SCHEMA + '.dn_visible_chars_begin',
                self.defaults['visible_chars_begin']
            )
        ))
        return result

    @visible_chars_begin.setter
    def visible_chars_begin(self, value):
        assert text_type(value).isdigit(), value

        self._set_session_param(
            CORE_SCHEMA + '.dn_visible_chars_begin',
            text_type(value)
        )

    @property
    def visible_chars_end(self):
        """Количество видимых символов в конце строки.

        Параметр используется функцией деперсонализации ``depersonalize_name``.

        :rtype: int
        """
        result = max(0, int(
            self._get_param(
                CORE_SCHEMA + '.dn_visible_chars_end',
                self.defaults['visible_chars_end']
            )
        ))
        return result

    @visible_chars_end.setter
    def visible_chars_end(self, value):
        assert text_type(value).isdigit(), value

        self._set_session_param(
            CORE_SCHEMA + '.dn_visible_chars_end',
            text_type(value)
        )

    @property
    def result_length(self):
        """Длина деперсонализированной строки.

        Если равна 0, то длина деперсонализированной строки будет равна
        длине исходной строки.

        Параметр используется функцией деперсонализации ``depersonalize_name``.

        :rtype: int
        """
        result = max(0, int(
            self._get_param(
                CORE_SCHEMA + '.dn_result_length',
                self.defaults['result_length']
            )
        ))
        return result

    @result_length.setter
    def result_length(self, value):
        assert text_type(value).isdigit(), value

        self._set_session_param(
            CORE_SCHEMA + '.dn_result_length',
            text_type(value)
        )

    @property
    def fill_char(self):
        """Символ-заполнитель.

        Параметр используется функцией деперсонализации ``depersonalize_name``.

        :rtype: unicode
        """
        result = self._get_param(
            CORE_SCHEMA + '.dn_fill_char',
            self.defaults['fill_char']
        )
        return result

    @fill_char.setter
    def fill_char(self, value):
        self._set_session_param(
            CORE_SCHEMA + '.dn_fill_char',
            text_type(value)
        )
# -----------------------------------------------------------------------------


class _D15nMode(object):

    """Менеджер контекста, переводящий БД в режим деперсонализации.

    При включении выполняются следующие действия:

        - добавляет в параметр ``search_path`` текущей сессии PostgreSQL
          схему, в которой размещаются деперсонализирующие представления для
          таблиц Системы.

    .. note::

       Возможно использование вложенных менеджеров контекста. В этом случае
       переключение в режим деперсонализации будет осуществляться только
       в менеджере верхнего уровня.
    """

    def __init__(self, mode_manager):  # noqa: D107
        self._mode_manager = mode_manager
        self._top_level = True

    def __enter__(self):  # noqa: D105
        self._top_level = not self._mode_manager.status
        if self._top_level:
            self._mode_manager.switch_on()

        return self

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: D105
        if exc_type is None and self._top_level:
            self._mode_manager.switch_off()


class ModeManager(_ConnectionMixin):

    """Менеджер режима деперсонализации.

    Отвечает за переключение (включение/выключение) режима деперсонализации БД.
    """

    def _get_search_path(self):
        """Возвращает список схем БД, в которых осуществляется поиск объектов.

        :rtype: list
        """
        with self._cursor as cursor:
            cursor.callproc(
                'current_setting',
                (
                    'search_path',
                ),
            )
            return cursor.fetchone()[0].split(', ')

    def _set_search_path(self, search_path):
        """Настраивает список схем БД, в которых осуществляется поиск объектов.

        :param list search_path: список схем БД.
        """
        with self._cursor as cursor:
            cursor.callproc(
                'set_config',
                (
                    'search_path',
                    ', '.join(search_path),
                    False
                ),
            )

    @property
    def status(self):
        """Возвращает True, если включен режим деперсонализации.

        :rtype: bool
        """
        result = DATA_SCHEMA in self._get_search_path()
        return result

    def switch_on(self):
        """Включает режим деперсонализации в БД."""
        pre_switch_mode.send(
            sender=self.__class__,
            instance=self,
            alias=self.alias,
            mode=True,
        )

        search_path = self._get_search_path()
        if DATA_SCHEMA not in search_path:
            search_path.insert(0, DATA_SCHEMA)
            self._set_search_path(search_path)

        post_switch_mode.send(
            sender=self.__class__,
            instance=self,
            alias=self.alias,
            mode=True,
        )

    def switch_off(self):
        """Выключает режим деперсонализации в БД."""
        pre_switch_mode.send(
            sender=self.__class__,
            instance=self,
            alias=self.alias,
            mode=False,
        )

        search_path = self._get_search_path()
        if DATA_SCHEMA in search_path:
            search_path.remove(DATA_SCHEMA)
            self._set_search_path(search_path)

        post_switch_mode.send(
            sender=self.__class__,
            instance=self,
            alias=self.alias,
            mode=False,
        )

    def get_cm(self):
        """Возвращает менеджер контекста для переключения режимов.

        :rtype: m3_d15n.utils.D15nMode
        """
        result = _D15nMode(self)
        return result
# -----------------------------------------------------------------------------


class _MigrateObserverMixin(object):

    """Класс-примесь для выполнения действий до/после применения миграций.

    Если в классе реализован метод ``_berofe_migrate``, то он вызывается
    **перед** применением миграций. Аналогично метод ``_after_migrate``
    вызывается **после** применения всех миграций.
    """

    def __init__(self, *args, **kwargs):  # noqa: D107
        super(_MigrateObserverMixin, self).__init__(*args, **kwargs)

        assert (
            hasattr(self, '_before_migrate') or hasattr(self, '_after_migrate')
        )
        self.__database_alias = None
        self.__app_names = set()

        pre_migrate.connect(self.__pre_migrate_handler)
        post_migrate.connect(self.__post_migrate_handler)

    def __pre_migrate_handler(self, app_config, using, **kwargs):
        if not self.__app_names:
            self.__database_alias = using
            if hasattr(self, '_before_migrate'):
                self._before_migrate(self.__database_alias)
        else:
            assert self.__database_alias == using

        self.__app_names.add(app_config.name)

    def __post_migrate_handler(self, app_config, using, **kwargs):
        assert self.__database_alias == using

        self.__app_names.remove(app_config.name)

        if not self.__app_names:
            pre_migrate.disconnect(self.__pre_migrate_handler)
            post_migrate.disconnect(self.__post_migrate_handler)

            if hasattr(self, '_after_migrate'):
                self._after_migrate(self.__database_alias)
# -----------------------------------------------------------------------------


class FieldsManager(_ConnectionMixin, _MigrateObserverMixin):

    """Менеджер деперсонализируемых полей.

    Предоставляет средства для настройки деперсонализации полей моделей Django.

    .. automethod:: __init__
    """

    def __init__(self, database_alias, sync_app_params):
        """Инициализация экземпляра класса.

        :param str database_alias: алиас базы данных в Django.
        :param bool sync_app_params: флаг, указывающий на необходимость
            синхронизации параметров деперсонализации полей. Параметры
            деперсонализации указываются в django-приложениях проекта в модулях
            ``d15n.py``.
        """
        super(FieldsManager, self).__init__(database_alias)

        self._config_synchronized = False
        if sync_app_params:
            connection_created.connect(self._on_connection_created)
            post_install.connect(self._on_connection_created)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _get_model_by_table_name(self, table_name):
        """Возвращает модель по имени таблицы в БД."""
        for model in apps.get_models(include_auto_created=True,
                                     include_swapped=True):
            # pylint: disable=protected-access
            if (
                model._meta.db_table == table_name and
                router.db_for_write(model) == self.alias
            ):
                result = model
                break
        else:  # pragma: no cover
            result = None

        return result

    def get_config(self):
        """Возвращает текущую конфигурацию подсистемы деперсонализации.

        :returns: Словарь вида

            .. code-block:: python

               {
                   model_class: (
                       (model_field, func_params),
                       ...
                   ),
                   ...
               }
        :rtype: dict
        """
        result = {}

        with self._cursor as cursor:
            cursor.execute("""
                select
                    table_name,
                    column_name,
                    function_params
                from
                    {core_schema}.columns_config_as_names
                order by
                    table_name
            """.format(
                core_schema=CORE_SCHEMA,
            ))

            for table, fields in groupby(cursor, itemgetter(0)):
                model = self._get_model_by_table_name(table)
                result[model] = {
                    (field, func_params)
                    for _, field, func_params in fields
                }

        return result
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def add_field(self, field, function_name, function_params=''):
        """Добавляет поле в параметры деперсонализации.

        :param field: поле модели.
        :type field: django.db.models.fields.Field

        :param basestring function_name: имя деперсонализирующей функции в БД,
            например ``'d15_core.depersonalize_name'``.

        :param basestring function_params: параметры деперсонализирующей
            функции. Строка вставляется в вызов функции "как есть", поэтому
            можно использовать любые выражения PostgreSQL.
        """
        pre_add_field.send(
            sender=self.__class__,
            instance=self,
            field=field,
            function_name=function_name,
            function_params=function_params,
        )

        with self._cursor as cursor:
            cursor.execute("""
                insert into {core_schema}.columns_config (
                    table_oid,
                    column_name,
                    function_oid,
                    function_params
                ) values (
                    'public.{table_name}'::regclass::oid,
                    '{column_name}',
                    to_regproc('{function_name}'),
                    %s
                )
            """.format(
                # pylint: disable=protected-access
                core_schema=CORE_SCHEMA,
                table_name=field.model._meta.db_table,
                column_name=field.column,
                function_name=function_name,
            ), [function_params])

        post_add_field.send(
            sender=self.__class__,
            instance=self,
            field=field,
            function_name=function_name,
            function_params=function_params,
        )

    def delete_field(self, field):
        """Удаляет поле модели из параметров деперсонализации.

        :param field: поле модели
        :type field: django.db.models.fields.Field
        """
        pre_delete_field.send(
            sender=self.__class__,
            instance=self,
            field=field,
        )

        # pylint: disable=protected-access
        with self._cursor as cursor:
            cursor.callproc(
                CORE_SCHEMA + '.get_table_schema',
                (
                    field.model._meta.db_table,
                )
            )
            table_schema = cursor.fetchone()[0]
            cursor.execute("""
                delete from {core_schema}.columns_config
                where
                    table_oid = '{table_schema}.{table_name}'::regclass and
                    column_name = '{column_name}'
            """.format(
                core_schema=CORE_SCHEMA,
                table_schema=table_schema,
                table_name=field.model._meta.db_table,
                column_name=field.column,
            ))

        post_delete_field.send(
            sender=self.__class__,
            instance=self,
            field=field,
        )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _clean_config(self):
        """Удаляет из конфигурации неактуальные записи.

        После восстановления БД из дампа может возникнуть ситуация, когда
        oid-ы таблиц или функций поменяются. В этом случае записи в таблице
        ``columns_config`` теряют актуальность и подлежат удалению.
        """
        with self._connection.cursor() as cursor:
            cursor.execute("""
                delete from "{}"."columns_config"
                where
                    table_oid not in (select oid from pg_catalog.pg_class) or
                    function_oid not in (select oid from pg_catalog.pg_proc)
            """.format(CORE_SCHEMA))

    def _collect_system_config(self):
        """Возвращает параметры деперсонализации, определенные в Системе.

        :param connection: Подключение к БД. Определяет, какие модели нужно
            учитывать при сборе параметров.

        :raises ValueError: если для одного и того же поля в разных приложениях
            заданы разные параметры деперсонализации.

        :returns: кортежи следующего вида:

            .. code-block:: python

               (app_label, model_name, field_name, func_name, func_params)
        :rtype: generator of tuple
        """
        for app in apps.get_app_configs():
            try:
                d15n_module = import_module(app.module.__name__ + '.d15n')
            except ImportError as error:
                if text_type(error).startswith('No module named '):
                    continue
                raise  # pragma: no cover

            if not hasattr(d15n_module, 'field_params'):
                continue  # pragma: no cover

            for model, fields_params in iteritems(d15n_module.field_params):
                assert isinstance(model, Iterable), model
                assert len(model) == 2, model
                model = apps.get_model(*model)

                if router.db_for_write(model) != self.alias:
                    continue

                for field_params in fields_params:
                    assert isinstance(field_params, Iterable), field_params
                    assert len(field_params) in (2, 3), field_params

                    # pylint: disable=protected-access
                    params = (
                        model._meta.app_label,
                        model._meta.object_name,
                        model._meta.get_field(field_params[0]).name,
                    )
                    if len(field_params) == 2:
                        params += (field_params[1], '')
                    elif len(field_params) == 3:
                        params += (field_params[1:])

                    yield params

    def _get_current_config(self):
        """Возвращает параметры деперсонализации, определенные в БД.

        :returns: кортежи следующего вида:

            .. code-block:: python

               (app_label, model_name, field_name, func_name, func_params)
        :rtype: generator
        """
        with self._connection.cursor() as cursor:
            cursor.execute("""
                select
                    table_name,
                    column_name,
                    function_schema,
                    function_name,
                    function_params
                from
                    {}.columns_config_as_names
            """.format(CORE_SCHEMA))
            for (
                table_name, column_name,
                function_schema, function_name, function_params
            ) in cursor:
                model = self._get_model_by_table_name(table_name)
                if not model:  # pragma: no cover
                    continue

                # pylint: disable=protected-access
                yield (
                    model._meta.app_label,
                    model._meta.object_name,
                    model._meta.get_field(column_name).name,
                    function_schema + '.' + function_name,
                    function_params or ''
                )

    def _add_fields_to_db(self, params):
        """Добавляет новые поля в конфигурацию БД."""
        # pylint: disable=protected-access
        for app, model, field, func_name, func_params in params:
            model = apps.get_model(app, model)
            field = model._meta.get_field(field)
            assert field.concrete, (app, model, field)

            self.add_field(field, func_name, func_params)

    def _delete_fields_from_db(self, params):
        """Удаляет поля из конфигурации БД."""
        # pylint: disable=protected-access
        for app, model, field, _, _ in params:
            model = apps.get_model(app, model)
            field = model._meta.get_field(field)
            assert field.concrete, (app, model, field)

            self.delete_field(field)

    def sync_config(self, force=False):
        """Выполняет синхронизацию параметров деперсонализации полей.

        На первом этапе синхронизации выполняется сбор параметров
        деперсонализации во всех подключенных к Системе приложениях. Для этого
        в каждом приложении осуществляется поиск модулей ``d15n.py``, в которых
        должен быть определен параметр ``FIALD_PARAMS``, содержащий словарь
        следующего вида:

        .. code-block:: python

           field_params = {
               ('person', 'Person'): (
                   ('surname', FUNC_DEPERSONALIZE_NAME),
                   ('firstname', FUNC_DEPERSONALIZE_NAME),
                   ('patronymic', FUNC_DEPERSONALIZE_NAME),
                   ('snils', FUNC_DEPERSONALIZE_NON_PUNCTUATION, "'x'"),
                   ('photo', FUNC_DEPERSONALIZE_TO_EMPTY_STRING),
                   ('photo_height', FUNC_DEPERSONALIZE_TO_NULL),
                   ('photo_width', FUNC_DEPERSONALIZE_TO_NULL),
                   ('act_address', FUNC_DEPERSONALIZE_TO_NULL),
                   ('reg_address', FUNC_DEPERSONALIZE_TO_NULL),
                   ('tmp_address', FUNC_DEPERSONALIZE_TO_NULL),
               ),
           }

        Затем осуществляется сверка параметров, определенных в Системе, с
        параметрами, указанными в БД (таблица ``columns_config``). При
        нахождении различий осуществляются соответствующие изменения в БД.

        :param bool force: флаг, указывающий на необходимость принудительной
            синхронизации вне зависимости от того, что синхронизация уже была
            выполнена ранее.
        """
        if not force and self._config_synchronized:
            return

        with Lock(self._connection), atomic(self.alias):
            system_params = set(self._collect_system_config())
            db_params = set(self._get_current_config())

            if system_params != db_params:
                with _SuspendConfigTriggers(self._connection):
                    # Удаление неактуальных записей из конфигурации.
                    self._clean_config()

                    # Удаление столбцов, исключенных из конфигурации.
                    self._delete_fields_from_db(db_params - system_params)

                    # Добавление новых столбцов.
                    self._add_fields_to_db(system_params - db_params)

                with self._connection.cursor() as cursor:
                    cursor.callproc(CORE_SCHEMA + '.update_views_set')

        self._config_synchronized = True

    def _on_connection_created(self, **kwargs):
        """Синхронизирует системные параметры деперсонализации с БД.

        Вызывается через сигналы
        :obj:`~django.db.backends.signals.connection_created` и
        :obj:`~m3_d15n.utils.post_install`.
        """
        if 'connection' in kwargs:
            alias = kwargs['connection'].alias
        elif 'alias' in kwargs:  # pragma: no cover
            alias = kwargs['alias']
        else:  # pragma: no cover
            raise ValueError()

        if not is_in_migration_command():
            if alias == self.alias and _is_initialized(alias):
                self.sync_config()

                connection_created.disconnect(self._on_connection_created)
                post_install.disconnect(self._on_connection_created)

    def _after_migrate(self, database_alias):
        """Синхронизирует системные параметры деперсонализации с БД.

        См. также ``_MigrateObserverMixin``.
        """
        if self.alias == database_alias and _is_initialized(database_alias):
            self.sync_config()
# -----------------------------------------------------------------------------


class _PgACLEntry(object):

    """Элемент списка управления доступом PostgreSQL."""

    # Функции PostgreSQL has_*_privilege в данном случае не используются,
    # т.к. они возвращают true в и том случае, если объект общедоступен
    # (есть доступ у public). Но если в дальнейшем доступ у public будет
    # отозван, то у непривилегированного пользователя доступ также пропадет.
    #
    # Чтобы избежать таких ситуаций, доступ непривилегированного пользователя
    # к объекту выдается вне зависимости от общедоступности этого объекта. Но
    # для того, чтобы узнать, был ли ранее выдан доступ, приходится вручную
    # разбирать данные соответствующего столбца.

    _privileges_map = {
        'r': 'SELECT',
        'w': 'UPDATE',
        'a': 'INSERT',
        'd': 'DELETE',
        'D': 'TRUNCATE',
        'x': 'REFERENCES',
        't': 'TRIGGER',
        'X': 'EXECUTE',
        'U': 'USAGE',
        'C': 'CREATE',
        'c': 'CONNECT',
        'T': 'TEMPORARY',
    }

    def __init__(self, entry):
        self.grantee, self.privileges, self.grantor = self._parse(entry)

    def _parse(self, entry):
        grantee, _, entry = entry.partition('=')
        grantee = grantee or 'PUBLIC'
        privileges, _, grantor = entry.rpartition('/')

        if any(
            privilege not in self._privileges_map
            for privilege in privileges
            if privilege != '*'
        ):
            raise ValueError('Invalid privileges: ' + privileges)

        privileges = frozenset(
            self._privileges_map[privilege]
            for privilege in privileges
            if privilege in self._privileges_map
        )

        return grantee, privileges, grantor

    def __eq__(self, other):
        return (
            isinstance(other, _PgACLEntry) and
            self.grantee.upper() == other.grantee.upper() and
            self.privileges == other.privileges and
            self.grantor.upper() == other.grantor.upper()
        )

    def __repr__(self):  # pragma: no cover
        return 'ACLEntry({}={}/{})'.format(
            self.grantee,
            ','.join(self.privileges),
            self.grantor,
        )

    def __str__(self):  # pragma: no cover
        short_privileges = ''.join(
            short
            for short, full in iteritems(self._privileges_map)
            if full in self.privileges
        )
        return '{}={}/{}'.format(
            self.grantee if self.grantee != 'PUBLIC' else '',
            short_privileges,
            self.grantor,
        )


class _PgACL(object):

    """Список доступа PostgreSQL."""

    def __init__(self, acl):
        if isinstance(acl, string_types):
            acl = acl.split(',')

        self.acl = tuple(
            _PgACLEntry(entry)
            for entry in acl
        )

    def __contains__(self, obj):
        if isinstance(obj, string_types):
            # Имя получателя прав (grantee).
            result = any(
                obj.upper() == entry.grantee.upper()
                for entry in self.acl
            )
        elif isinstance(obj, _PgACLEntry):
            result = obj in self.acl
        elif isinstance(obj, tuple) and len(obj) == 2:
            grantee, privileges = obj
            if isinstance(privileges, string_types):
                privileges = (privileges,)
            privileges = {p.upper() for p in privileges}
            result = any(
                privilege in privileges
                for entry in self.get_by_grantee(grantee)
                for privilege in entry.privileges
            )
        else:  # pragma: no cover
            raise TypeError(obj)

        return result

    def get_by_grantee(self, name):
        """Возвращает элементы списка по имени получателя прав доступа.

        :param str name: имя получателя прав доступа.

        :rtype: generator
        """
        for entry in self.acl:
            if entry.grantee.upper() == name.upper():
                yield entry

    def get_by_grantor(self, name):
        """Возвращает элементы списка по имени пользователя, выдавшего права.

        :param str name: имя пользователя, выдавшего права.

        :rtype: generator
        """
        for entry in self.acl:
            if entry.grantor.upper() == name.upper():
                yield entry

    def get_by_privileges(self, *privileges):
        """Возвращает элементы списка, содержащие указанные права доступа.

        :param privileges: права доступа.

        :rtype: generator
        """
        for entry in self.acl:
            if entry.privileges.issuperset(
                privilege.upper() for privilege in privileges
            ):
                yield entry

    def __len__(self):
        return len(self.acl)

    def __getitem__(self, index):  # pragma: no cover
        return self.acl[index]

    def __iter__(self):  # pragma: no cover
        return iter(self.acl)

    def __repr__(self):  # pragma: no cover
        return 'ACL({})'.format(','.join(repr(entry) for entry in self.acl))


class _UserAccessManager(_ConnectionMixin):

    """Менеджер прав доступа к объектам БД."""

    # Системные схемы PostgreSQL.
    _system_schemas = (
        'pg_catalog',
        'information_schema',
        'pg_temp_1',
        'pg_toast',
        'pg_toast_temp_1',
    )
    _system_schemas_sql = '({})'.format(','.join(map(
        lambda s: str(QuotedString(s)),
        _system_schemas
    )))

    def __init__(self, database_alias, user_name):
        """Инициализация экземпляра класса.

        :param str database_alias: Алиас деперсонализируемой базы
            данных.
        :param str user_name: Имя пользователя.
        """
        super(_UserAccessManager, self).__init__(database_alias)
        self.user_name = user_name
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _has_object_access(self, function, object_name, privilege):
        with self._cursor as cursor:
            cursor.callproc(function, (self.user_name, object_name, privilege))
            return cursor.fetchone()[0]

    def has_database_access(self):
        """Возвращает True, если есть разрешение на подключение к БД.

        :rtype: bool
        """
        return self._has_object_access(
            'has_database_privilege', self._dbname, 'connect'
        )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def get_schemas(self):
        """Возвращает имена схем с их разрешениями.

        :rtype: generator
        """
        with self._cursor as cursor:
            cursor.execute("""
                select
                    oid::regnamespace schema_name,
                    nspacl::text[]
                from
                    pg_catalog.pg_namespace
                where
                    oid::regnamespace not in {}
            """.format(
                self._system_schemas_sql,
            ))

            for schema, acl in cursor:
                yield schema, None if acl is None else _PgACL(acl)

    def get_columns(self):
        """Возвращает столбцы с их разрешениями.

        :rtype: dict
        """
        with self._cursor as cursor:
            # Загрузка деперсонализированных полей
            cursor.execute("""
                select
                    table_oid::regclass::name,
                    array_agg(column_name)
                from
                    d15n_core.columns_config
                group by table_oid
            """.format(
                core_schema=CORE_SCHEMA,
            ))
            depersonalized_fields = {
                table_name: set(column_names)
                for table_name, column_names in cursor
            }

            cursor.execute("""
                select
                    attrelid::regclass::name,
                    attname,
                    attacl::text[]
                from pg_catalog.pg_attribute
                where
                    not attisdropped and
                    attnum > 0 and
                    attrelid in (
                        select table_oid
                        from d15n_core.columns_config
                    )
                order by attnum
            """.format(
                core_schema=CORE_SCHEMA,
            ))
            result = defaultdict(list)
            for table_name, column_name, acl in cursor:
                result[table_name].append((
                    column_name,
                    None if acl is None else _PgACL(acl),
                    column_name in depersonalized_fields[table_name]
                ))

        return result

    def get_tables(self):
        """Возвращает имена таблиц, их разрешения и последовательности.

        :rtype: generator
        """
        with self._cursor as cursor:
            cursor.execute("""
                select
                    c.oid::regclass::name,
                    c.relacl::text[],
                    array(
                        select
                            pg_get_serial_sequence(
                                c.oid::regclass::name, a.attname
                            )
                        from
                            pg_index i
                            join pg_attribute a on (
                                a.attrelid = i.indrelid and
                                a.attnum = any(i.indkey)
                            )
                        where i.indrelid = c.oid and i.indisprimary
                    )
                from
                    pg_catalog.pg_class c
                where
                    c.relkind in ('r', 'f')
                    and c.relnamespace::regnamespace not in {}
            """.format(
                self._system_schemas_sql,
            ))

            for table_name, acl, sequences in cursor:
                yield (
                    table_name,
                    None if acl is None else _PgACL(acl),
                    filter(None, sequences)
                )

    def get_views(self):
        """Возвращает представления с их разрешениями.

        :rtype: generator
        """
        with self._cursor as cursor:
            cursor.execute("""
                select
                    oid::regclass,
                    relacl::text[]
                from pg_catalog.pg_class
                where
                    relkind = 'v'::char and
                    relnamespace::regnamespace not in {}
            """.format(
                self._system_schemas_sql,
            ))

            for view_name, acl in cursor:
                yield view_name, None if acl is None else _PgACL(acl)

    def get_functions(self):
        """Возвращает функции, на которые есть/отсутствует привилегия.

        :rtype: generator
        """
        with self._cursor as cursor:
            cursor.execute("""
                select
                    oid::regprocedure,
                    proacl::text[]
                from pg_catalog.pg_proc
                where
                    pronamespace::regnamespace not in {}
            """.format(
                self._system_schemas_sql,
            ))

            for view_name, acl in cursor:
                yield view_name, None if acl is None else _PgACL(acl)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _set_access(self, grant, object_type, object_name, *privileges):
        with self._cursor as cursor:
            cursor.execute("""
                {} {} on {} {} {} {}
            """.format(
                'grant' if grant else 'revoke',
                ', '.join(privileges),
                object_type,
                object_name,
                'to' if grant else 'from',
                self.user_name,
            ))

    def grant(self, object_type, object_name, *privileges):
        """Выдает разрешения на доступ к указанным объектам.

        :param str object_type: тип объекта (``'database'``, ``'schema'``,
            ``'table'``, ``'view'``, ``'function'``).

        :param str object_name: имя объекта (для таблиц, представлений и
            функций предпочительно также указывать схему:
            ``"schema_name"."object_name"``).

        :param privileges: привилегии (``'select'``, ``'update'``, ``'usage'``,
            ``'connect'`` и т.д.).
        """
        self._set_access(True, object_type, object_name, *privileges)

    def revoke(self, object_type, object_name, *privileges):
        """отзывает разрешения на доступ к указанным объектам.

        :param str object_type: тип объекта (``'database'``, ``'schema'``,
            ``'table'``, ``'view'``, ``'function'``).

        :param str object_name: имя объекта (для таблиц, представлений и
            функций предпочительно также указывать схему:
            ``"schema_name"."object_name"``).

        :param privileges: привилегии (``'select'``, ``'update'``, ``'usage'``,
            ``'connect'`` и т.д.).
        """
        self._set_access(False, object_type, object_name, *privileges)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class UnprivilegedModeManager(_MigrateObserverMixin, _ConnectionMixin):

    """Менеджер режима непривилегированного пользователя.

    Предоставляет средства для настройки прав доступа непривилегированного
    пользователя, а также переключения между основным и непривилегированным
    пользователями.

    Непривилегированный пользоватеь может использоваться двумя способами:
    постоянное подключение и временное переключение при переходе в режим
    деперсонализации. Права доступа непривилегированного пользователя
    настраиваются так, чтобы у него не было доступа к деперсонализируемым
    данным. Для этого отзываются права доступа к таблицам с данными и
    предоставляется доступ к деперсонализирующим представлениям. Такая схема
    даёт дополнительную защиту от случайного предоставления доступа к исходным
    данным в режиме деперсонализации.

    .. automethod:: __init__
    """

    def __init__(self, database_alias, unprivileged_user, switch_users):
        """Инициализация класса.

        :param str database_alias: Алиас деперсонализируемой базы
            данных.
        :param str unprivileged_user: Имя непривилегированного пользователя
            PostgreSQL.
        :param bool switch_users: флаг, указывающий на необходимость
            переключения на непривилегированную учетную запись СУБД при
            включении режима деперсонализации.
        """
        assert unprivileged_user, unprivileged_user

        super(UnprivilegedModeManager, self).__init__(database_alias)

        self.unprivileged_user = unprivileged_user

        if not is_in_migration_command():
            connection_created.connect(self._on_connection_created)
            post_install.connect(self._on_connection_created)

        if switch_users:
            post_switch_mode.connect(self._on_mode_switch)

        post_add_field.connect(self._on_fields_config_changed)
        post_delete_field.connect(self._on_fields_config_changed)

    def _on_connection_created(self, **kwargs):
        """Настраивает разрешения непривилегированного пользователя.

        Вызывается через сигналы
        :obj:`~django.db.backends.signals.connection_created` и
        :obj:`~m3_d15n.utils.post_install`.
        """
        if 'connection' in kwargs:
            alias = kwargs['connection'].alias
        elif 'alias' in kwargs:  # pragma: no cover
            alias = kwargs['alias']
        else:  # pragma: no cover
            raise ValueError()

        if alias == self.alias:
            self.grant()

            connection_created.disconnect(self._on_connection_created)
            post_install.disconnect(self._on_connection_created)

    def _after_migrate(self, database_alias):
        """Восстанавливает деперсонализирующие представления."""
        if database_alias == self.alias and _is_initialized(database_alias):
            self.grant()

    def _on_fields_config_changed(self, field, **kwargs):
        """Перенастраивает права доступа при изменении конфигурации полей."""
        alias = router.db_for_write(field.model)
        if self.alias == alias:
            self.grant()

    def _on_mode_switch(self, alias, mode, **kwargs):
        """Переключает пользователей при переключении режима деперсонализации.

        .. seealso::

           :obj:`~m3_d15n.utils.post_switch_mode`.
        """
        if self.alias == alias:
            if mode:
                self.switch_on()
            else:
                self.switch_off()

    def is_switchable(self):
        """Возвращает True, если доступно переключение между пользователями.

        Возможность переключения доступна только в том случае, когда имя
        основного пользователя БД, указанного в параметре :setting:`DATABASES`
        """
        main_user = settings.DATABASES[self.alias]['USER']
        return self.unprivileged_user and self.unprivileged_user != main_user

    @atomic
    def _set_access(self, grant):
        """Выдача/отзыв доступа для непривилегированного пользователя.

        Доступ предоставляется ко всем объектам, кроме деперсонализированных
        таблиц.

        :param bool grant: флаг, определяющий выдачу или отзыв привилегий (
            ``True`` --- выдача, ``False`` --- отзыв).
        """
        # pylint: disable=too-many-statements
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        privileges = ('select', 'insert', 'update', 'delete')

        am = _UserAccessManager(self.alias, self.unprivileged_user)

        if _is_initialized(self.alias):
            columns_by_table = am.get_columns()
        else:
            columns_by_table = {}  # pragma: no cover
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Инверсия операций предоставления/отзыва доступа к зависимости от
        # значения аргумента grant.
        access_action = am.grant if grant else am.revoke
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Доступ к базе данных.
        if am.has_database_access() != grant:
            access_action(
                'database',
                quote_ident(self._dbname, self._connection.connection),
                'connect'
            )
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Доступ к схемам базы данных.
        for schema, acl in am.get_schemas():
            accessible = acl is not None and (am.user_name, 'usage') in acl
            if grant != accessible:
                access_action('schema', schema, 'usage')
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Доступ к таблицам.

        def is_selectable(acl):
            return acl is not None and (am.user_name, 'select') in acl

        def is_changable(acl):
            return (
                acl is not None and
                (am.user_name, 'insert') in acl and
                (am.user_name, 'update') in acl and
                (am.user_name, 'delete') in acl
            )

        for table, acl, sequences in am.get_tables():
            selectable = is_selectable(acl)
            changable = is_changable(acl)

            if table == CORE_SCHEMA + '.columns_config':  # pragma: no cover
                if grant != selectable:
                    access_action('table', table, 'select')
                if changable:
                    am.revoke('table', table, 'insert', 'update', 'delete')
            elif grant:  # Выдача доступа ко всем таблицам.
                if table in columns_by_table:
                    if selectable:
                        am.revoke('table', table, 'select')
                    if not changable:
                        am.grant('table', table, 'insert', 'update', 'delete')
                    if selectable or not changable:
                        for sequence in sequences:
                            am.grant('sequence', sequence, 'usage')
                else:
                    # Обычные таблицы доступны для чтения и изменения.
                    if not selectable or not changable:
                        am.grant('table', table, *privileges)
                        for sequence in sequences:
                            am.grant('sequence', sequence, 'usage')
            else:  # Отзыв разрешений.
                am.revoke('table', table, *privileges)
                for sequence in sequences:
                    am.revoke('sequence', sequence, 'usage')

            if table in columns_by_table:
                # Таблица деперсонализирована, поэтому нужно разрешить
                # чтение для НЕдеперсонализированных полей.
                columns = columns_by_table[table]
                for col_name, col_acl, col_depersonalized in columns:
                    select = 'select("{}")'.format(col_name)
                    selectable = is_selectable(col_acl)
                    if col_depersonalized == grant and selectable:
                        am.revoke('table', table, select)
                    elif not col_depersonalized and grant and not selectable:
                        am.grant('table', table, select)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Доступ к представлениям.
        for view, acl in am.get_views():
            if view == CORE_SCHEMA + '.columns_config_as_names':
                if grant != is_selectable(acl):
                    access_action('table', view, 'select')
                if is_changable(acl):
                    am.revoke(
                        'table', view, 'insert', 'update', 'delete'
                    )  # pragma: no cover
            else:
                accessible = (
                    acl is not None and
                    (am.user_name, 'select') in acl
                )
                if grant != accessible:
                    access_action('table', view, *privileges)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Доступ к функциям.
        for function, acl in am.get_functions():
            accessible = acl is not None and (am.user_name, 'execute') in acl
            if grant != accessible:
                access_action('function', function, 'execute')
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def grant(self):
        """Выдает доступ к объектам Системы.

        Выдача прав осуществляется к следующим объектам базы данных, указанной
        при создании экземпляра класса (аргумент ``database_alias``):

            * базе данных;
            * схемам этой базы данных;
            * всем таблицам и последовательностям, связанным с первичными
              ключами этих таблиц;
            * представлениям;
            * функциям.

        Доступ выдается непривилегированному пользователю, указанному при
        создании экземпляра класса, от имени текущего пользователя, указанного
        в параметрах подключения к БД в конфигурации проекта Django.
        """
        with Lock(self._connection):
            self._set_access(True)

    def revoke(self):
        """Отзывает доступ к объектам Системы.

        Отзыв прав осуществляется у следующих объектов базы данных, указанной
        при создании экземпляра класса (аргумент ``database_alias``):

            * базы данных;
            * схем этой базы данных;
            * всех таблиц и последовательностей, связанных с первичными
              ключами этих таблиц;
            * представлений;
            * функций.

        Доступ отзывается у непривилегированного пользователя, указанного при
        создании экземпляра класса, от имени текущего пользователя, указанного
        в параметрах подключения к БД в конфигурации проекта Django.
        """
        with Lock(self._connection):
            self._set_access(False)

    def _switch_user(self, user):
        with self._cursor as cursor:
            cursor.execute('set role ' + quote_ident(user, cursor.cursor))

    def switch_on(self):
        """Переключает соединение с БД на непривилегированного пользователя."""
        self._switch_user(self.unprivileged_user)

    def switch_off(self):
        """Переключает соединение с БД на привилегированного пользователя."""
        self._switch_user(settings.DATABASES[self.alias]['USER'])
# -----------------------------------------------------------------------------


class DatabaseManager(_ConnectionMixin):

    """Менеджер базы данных.

    Предоставляет средства для установки подсистемы в БД и её удаления, а также
    синхронизации параметров деперсонализации полей, определенных в Системе, с
    параметрами в БД.

    .. automethod:: __init__
    """

    def _execute_sql_file(self, file_name, **params):  # pragma: no cover
        file_path = join(dirname(__file__), file_name)

        with codecs.open(file_path, 'r', 'utf-8') as sql_file:
            sql = sql_file.read()

        sql = sql.replace('{}', '{{}}')
        sql = sql.format(**params)

        with self._cursor as cursor:
            cursor.execute(sql)

    @atomic
    def install(self):  # pragma: no cover
        """Устанавливает в БД необходимые для работы подсистемы объекты.

        Описание объектов (функций, таблиц, представлений, триггеров и т.п.)
        находится в файле ``sql/main.sql``.

        .. seealso::

           :obj:`~m3_d15n.utils.pre_install`,
           :obj:`~m3_d15n.utils.post_install`.
        """
        pre_install.send(
            sender=self.__class__, instance=self, alias=self.alias
        )
        self._execute_sql_file(
            'sql/main.sql',
            core_schema=CORE_SCHEMA,
            data_schema=DATA_SCHEMA,
        )
        post_install.send(
            sender=self.__class__, instance=self, alias=self.alias
        )

    def uninstall(self):
        """Удаляет из БД объекты подсистемы деперсонализации.

        Для этого удаляются схемы с именами, указанными в
        :obj:`~m3_d15n.constants.CORE_SCHEMA` и
        :obj:`~m3_d15n.constants.DATA_SCHEMA`.

        .. seealso::

           :obj:`~m3_d15n.utils.pre_uninstall`,
           :obj:`~m3_d15n.utils.post_uninstall`.
        """
        pre_uninstall.send(
            sender=self.__class__, instance=self, alias=self.alias
        )
        with self._cursor as cursor:
            for schema in (DATA_SCHEMA, CORE_SCHEMA):
                cursor.execute(
                    'drop schema if exists {} cascade'.format(schema)
                )
        post_uninstall.send(
            sender=self.__class__, instance=self, alias=self.alias
        )
# -----------------------------------------------------------------------------


class D15nManager(object):

    """Менеджер подсистемы деперсонализации.

    Предоставляет средства для установки и удаления из БД подсистемы
    деперсонализации, а также запроса сведений о её состоянии.

    .. automethod:: __init__
    """

    def __init__(self, database_alias, sync_app_params=False,
                 unprivileged_user=None, switch_users=False,
                 default_params=None):
        """Инициализация менеджера подсистемы деперсонализации.

        :param database_alias: алиас подключения к БД в Django.
        :type database_alias: str

        :param sync_app_params: флаг, указывающий на необходимость
            синхронизации параметров при подключении к БД.
        :type sync_app_params: bool

        :param unprivileged_user: имя непривилегированной роли PostgreSQL.
        :type unprivileged_user: str or None

        :param switch_users: флаг, указывающий на необходимость переключения
            на непривилегированную учетную запись СУБД при включении
            режима деперсонализации.

            При использовании привилегированной учетной записи в неё должна
            быть добавлена непривилегированная учетная запись:

            .. code-block:: sql

               grant <unprivileged> to <privileged>
        :type switch_users: bool

        :param default_params: значения по умолчанию глобальных параметров
            деперсонализации.
        :type default_params: dict or None
        """
        assert database_alias in settings.DATABASES, database_alias

        database_settings = settings.DATABASES[database_alias]

        self.database_alias = database_alias
        self.sync_app_params = sync_app_params
        self.unprivileged_user = unprivileged_user
        self.switch_users = switch_users
        self.default_params = default_params

        self.params = ParamsManager(
            self.database_alias, self.default_params or {}
        )

        if (
            not unprivileged_user or
            database_settings.get('USER') != unprivileged_user
        ):
            self._database_manager = DatabaseManager(
                self.database_alias
            )
            self._fields_manager = FieldsManager(
                self.database_alias, self.sync_app_params
            )
            if self.unprivileged_user:
                self.unprivileged_mode_manager = UnprivilegedModeManager(
                    database_alias=self.database_alias,
                    unprivileged_user=self.unprivileged_user,
                    switch_users=self.switch_users,
                )

    def install(self):  # pragma: no cover
        """Устанавливает в БД необходимые для работы подсистемы объекты.

        .. seealso::

           :meth:`m3_d15n.utils.DatabaseManager.install`
        """
        return self._database_manager.install()

    def uninstall(self):
        """Удаляет из БД объекты подсистемы деперсонализации.

        .. seealso::

           :meth:`m3_d15n.utils.DatabaseManager.install`
        """
        return self._database_manager.uninstall()

    @cached_property
    def _mode_manager(self):
        """Менеджер режима деперсонализации.

        :rtype: m3_d15n.utils.ModeManager
        """
        return ModeManager(self.database_alias)

    def is_in_d15n_mode(self):  # pragma: no cover
        """Возвращает True, если включен режим деперсонализации.

        :rtype: bool
        """
        return self._mode_manager.status

    def switch_on(self):
        """Включает режим деперсонализации в БД."""
        return self._mode_manager.switch_on()

    def switch_off(self):
        """Выключает режим деперсонализации в БД."""
        return self._mode_manager.switch_off()

    @property
    def d15n_mode(self):
        """Менеджер контекста для перевода БД в режим деперсонализации.

        :rtype: m3_d15n.utils._D15nMode
        """
        return self._mode_manager.get_cm()

    def get_config(self):  # pragma: no cover
        """Возвращает текущую конфигурацию подсистемы деперсонализации.

        .. seealso::

           :meth:`m3_d15n.utils.FieldsManager.get_config`

        :rtype: dict
        """
        return self._fields_manager.get_config()

    def add_field(self, field, function_name, function_params=''):
        """Добавляет поле в параметры деперсонализации.

        :param field: поле модели.
        :type field: django.db.models.fields.Field

        :param basestring function_name: имя деперсонализирующей функции в БД,
            например ``'d15_core.depersonalize_name'``.

        :param basestring function_params: параметры деперсонализирующей
            функции. Строка вставляется в вызов функции "как есть", поэтому
            можно использовать любые выражения PostgreSQL.
        """
        return self._fields_manager.add_field(
            field, function_name, function_params
        )

    def delete_field(self, field):
        """Удаляет поле модели из параметров деперсонализации.

        :param field: поле модели
        :type field: django.db.models.fields.Field
        """
        return self._fields_manager.delete_field(field)

    def sync_config(self, force=False):
        """Выполняет синхронизацию параметров деперсонализации полей.

        .. seealso::

           :meth:`m3_d15n.utils.FieldsManager.sync_config`

        :param bool force: флаг, указывающий на необходимость принудительной
            синхронизации вне зависимости от того, что синхронизация уже была
            выполнена ранее.
        """
        return self._fields_manager.sync_config(force)


class D15nManagerRegistry(object):

    """Реестр менеджеров деперсонализации."""

    def __init__(self):  # noqa: D107
        self._managers = {}
        self._skip_handler = None

    def skip_request(self, environ):
        """Проверяет, необходимо ли пропустить деперсонализацию запроса.

        Если задан обработчик запросов, проверка делегируется ему.

        :param environ: Словарь с параметрами запроса.
        """
        if self._skip_handler:  # pragma: no cover
            return self._skip_handler(environ)

    def set_request_handler(self, handler):
        """Задает обработчик запросов.

        Обработчик должен быть callable-обьектом и принимать параметры
        запроса в виде словаря (параметр environ сигнала
        django.core.signals.request_started). В случае, если запрос должен быть
        деперсонализирован то обработчик должен возвращать None или False.

        :param handler: callable обьект
        """
        if handler and callable(handler):  # pragma: no cover
            self._skip_handler = handler

    def register(self, manager):
        """Регистрирует менеджер деперсонализации в реестре.

        :param manager: m3_d15n.utils.D15nManager
        """
        assert isinstance(manager, D15nManager), type(manager)

        self._managers[manager.database_alias] = manager

    def get(self, database_alias):
        """Возвращает менеджер деперсонализации для указанной БД.

        :param basestring database_alias: Алиас базы данных, для которой
            запрашивается менеджер.

        :rtype: m3_d15n.utils.D15nManager
        """
        return self._managers[database_alias]

    def __contains__(self, database_alias):
        """Возвращает True, если для указанной БД зарегистрирован менеджер.

        :param basestring database_alias: Алиас базы данных.

        :rtype: bool
        """
        return database_alias in self._managers

    def is_in_d15n_mode(self):
        """Возвращает True, если все базы данных в режиме деперсонализации.

        :rtype: bool
        """
        return all(
            manager.is_in_d15n_mode()
            for manager in itervalues(self._managers)
        )

    def switch_on(self):
        """Включает режим деперсонализации во всех менеджерах."""
        for manager in itervalues(self._managers):
            manager.switch_on()

    def switch_off(self):
        """Отключает режим деперсонализации во всех менеджерах."""
        for manager in itervalues(self._managers):
            manager.switch_off()

    @property
    def d15n_mode(self):
        """Возвращает менеджеры контекста для режима деперсонализации.

        Для каждого из зарегистрированных менеджеров деперсонализации создает
        менеджер контекста :class:`~m3_d15n.utils.D15nMode` и объединяет их.
        """
        if PY2:
            result = contextlib.nested(*(
                manager.d15n_mode
                for manager in self._managers.itervalues()
            ))
        else:
            result = contextlib.ExitStack()
            for manager in self._managers.values():
                result.enter_context(manager.d15n_mode)

        return result

    def add_field(self, field, function_name):
        """Добавляет поле в параметры деперсонализации.

        Менеджер деперсонализации выбирается с помощью роутера Django.

        :param field: поле модели.
        :type field: django.db.models.fields.Field

        :param basestring function_name: имя деперсонализирующей функции в БД,
            например ``'d15_core.depersonalize_name'``.
        """
        alias = router.db_for_write(field.model)
        manager = self._managers[alias]
        manager.add_field(field, function_name)

    def delete_field(self, field):
        """Удаляет поле модели из параметров деперсонализации.

        Менеджер деперсонализации выбирается с помощью роутера Django.

        :param field: поле модели
        :type field: django.db.models.fields.Field
        """
        alias = router.db_for_write(field.model)
        manager = self._managers[alias]
        manager.delete_field(field)

    def sync_config(self, force=False):
        """Выполняет синхронизацию параметров деперсонализации полей.

        .. seealso::

           :meth:`m3_d15n.utils.FieldsManager.sync_config`

        :param bool force: флаг, указывающий на необходимость принудительной
            синхронизации вне зависимости от того, что синхронизация уже была
            выполнена ранее.
        """
        for manager in itervalues(self._managers):
            manager.sync_config(force)


class D15nViewsCleaner(_MigrateObserverMixin, object):

    """Удаляет деперсонализирующие представления на время применения миграций.

    Т.к. деперсонализирующие представления блокируют некоторые изменения в БД,
    перед выполнением management-команды ``migrate`` эти представления
    нужно удалить, а по завершении команды --- восстановить.
    """

    def _before_migrate(self, database_alias):
        """Удаляет деперсонализирующие представления."""
        if _is_initialized(database_alias):
            self._drop_d15n_views(database_alias)

    def _after_migrate(self, database_alias):
        """Восстанавливает деперсонализирующие представления."""
        if _is_initialized(database_alias):
            self._create_d15n_views(database_alias)

    @staticmethod
    def _drop_d15n_views(database_alias):
        """Удаляет деперсонализирующие представления."""
        FieldConfig = apps.get_model('m3_d15n', 'FieldConfig')

        for table_name in FieldConfig.objects.using(
            database_alias
        ).values_list('table_name', flat=True).distinct():
            with connections[database_alias].cursor() as cursor:
                cursor.execute("""
                    drop view if exists {data_schema}.{table_name}
                """.format(
                    data_schema=DATA_SCHEMA,
                    table_name=table_name,
                ))

        # Установка параметра in_migration, сообщающего триггеру on_sql_drop о
        # том, что выполняется процесс миграции.
        with connections[database_alias].cursor() as cursor:
            cursor.callproc('set_config', (
                CORE_SCHEMA + '.in_migration', 'TRUE', False
            ))

    @staticmethod
    def _create_d15n_views(database_alias):
        """Создает деперсонализирующие представления."""
        with connections[database_alias].cursor() as cursor:
            cursor.callproc('set_config', (
                CORE_SCHEMA + '.in_migration', '', False
            ))

            cursor.callproc(CORE_SCHEMA + '.update_views_set')
