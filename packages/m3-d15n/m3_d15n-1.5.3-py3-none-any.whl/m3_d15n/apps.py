# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django import apps
from django.conf import settings
from django.core.signals import request_finished
from django.core.signals import request_started
from django.db.backends.signals import connection_created

from . import d15n_managers_registry
from .constants import URL_PREFIX


class AppConfig(apps.AppConfig):  # noqa: D101

    name = __name__.rpartition('.')[0]

    def __init__(self, *args, **kwargs):  # noqa: D107
        super(AppConfig, self).__init__(*args, **kwargs)

        self.d15n_mode = False
        self._cleaner = None

    @staticmethod
    def _is_db_user_unprivileged(database_alias):
        """Возвращает True, если учетная запись БД непривилегированная."""
        database_user = settings.DATABASES.get(database_alias, {}).get('USER')

        manager = d15n_managers_registry.get(database_alias)
        unprivileged_user = manager.unprivileged_user

        return (
            unprivileged_user and
            database_user == unprivileged_user
        )

    def _on_request_started(self, environ, **kwargs):
        """Включает режим деперсонализации.

        Вызывается через сигнал ``request_started``. Для запросов по адресам,
        начинающимся с :obj:`~m3_d15n.constants.URL_PREFIX`, включает режим
        деперсонализации данных.
        """
        if environ['PATH_INFO'].startswith(URL_PREFIX):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(URL_PREFIX):]
            if not d15n_managers_registry.skip_request(environ):
                for database_alias in settings.DATABASES:
                    if (
                        database_alias in d15n_managers_registry and
                        not self._is_db_user_unprivileged(database_alias)
                    ):
                        manager = d15n_managers_registry.get(database_alias)
                        manager.switch_on()
                        self.d15n_mode = True

    def _on_request_finished(self, **kwargs):
        """Отключает режим деперсонализации.

        Вызывается через сигнал ``request_finished``.
        """
        if self.d15n_mode:
            for database_alias in settings.DATABASES:
                if (
                    database_alias in d15n_managers_registry and
                    not self._is_db_user_unprivileged(database_alias)
                ):
                    manager = d15n_managers_registry.get(database_alias)
                    manager.switch_off()

                    self.d15n_mode = False

    def _on_connection_created(self, connection, **kwargs):
        """Включает режим деперсонализации при переподключении к БД.

        Необходимость включения режима деперсонализации обусловлена тем, что
        после начала обработки запроса Django может (в зависимости от настроек
        подключения к БД) переподключаться к БД. Т.к. параметры (в т.ч.
        ``search_path``) устанавливаются только на время текущего сеанса, то
        при переподключении они сбрасываются и значениям по умолчанию.
        """
        if connection.alias in d15n_managers_registry:
            manager = d15n_managers_registry.get(connection.alias)
            if (
                self._is_db_user_unprivileged(connection.alias) or
                self.d15n_mode
            ):
                manager.switch_on()
            else:
                manager.switch_off()

    def _init_views_cleaner(self):
        from .utils import D15nViewsCleaner

        self._cleaner = D15nViewsCleaner()

    def ready(self):  # noqa: D102
        super(AppConfig, self).ready()

        self._init_views_cleaner()

        request_started.connect(
            self._on_request_started,
            dispatch_uid='m3_d15n.AppConfig.request_started'
        )
        request_finished.connect(
            self._on_request_finished,
            dispatch_uid='m3_d15n.AppConfig.request_finished'
        )
        connection_created.connect(
            self._on_connection_created,
            dispatch_uid='m3_d15n.AppConfig.connection_created'
        )
