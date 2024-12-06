# coding: utf-8
from contextlib import closing
from importlib import import_module
from inspect import currentframe


# Модуль является временным контейнером функционала, который в будущем будет
# перенесен в пакет с общим инструментарием платформы M3 m3-utils.


def is_in_migration_command():
    """Возвращает True, если код выполняется в рамках миграций Django.

    :rtype: bool
    """
    from django.core.management import ManagementUtility
    from django.db.migrations.executor import MigrationExecutor

    def is_in_command(command):
        frame = currentframe()
        while frame:
            if 'self' in frame.f_locals:
                self_object = frame.f_locals['self']
                if isinstance(self_object, (command, MigrationExecutor)):
                    result = True
                    break

                elif isinstance(self_object, ManagementUtility):
                    # Срабатывает при использовании функции в AppConfig
                    if 'subcommand' in frame.f_locals:
                        subcommand = frame.f_locals['subcommand']
                        result = subcommand == 'migrate'
                        break

                elif isinstance(self_object, MigrationExecutor):
                    # Используется при запуске тестов
                    result = True
                    break

            frame = frame.f_back
        else:
            result = None

        return result

    for module_name in (
        'django.core.management.commands.migrate',
        'django.core.management.commands.makemigrations',
        'django.core.management.commands.sqlmigrate',
        'django.core.management.commands.showmigrations',
    ):
        if is_in_command(import_module(module_name).Command):
            result = True
            break
    else:
        result = False

    return result


class Lock(object):

    """Блокировка с помощью функции PostgreSQL ``pg_advisory_lock``."""

    def __init__(self, connection):
        self._connection = connection

    def __enter__(self):
        with closing(self._connection.cursor()) as cursor:
            cursor.callproc('pg_advisory_lock', (hash('m3-d15n'),))

    def __exit__(self, exc_type, exc_val, exc_tb):
        with closing(self._connection.cursor()) as cursor:
            cursor.callproc('pg_advisory_unlock', (hash('m3-d15n'),))
