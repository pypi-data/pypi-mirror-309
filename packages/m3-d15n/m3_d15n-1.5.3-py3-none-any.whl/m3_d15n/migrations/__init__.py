# coding: utf-8
from django.contrib.postgres.operations import HStoreExtension


# Флаг, указывающий на то, что во время текущего запуска подсистема уже была
# установлена в БД.
always_installed = False


# Флаг, указывающий на то, что во время текущего запуска подсистема уже была
# удалена из БД.
always_uninstalled = False


class PermanentHStoreExtension(HStoreExtension):

    """Операция по добавлению расширения hstore без удаления при откате."""

    def database_backwards(
        self, app_label, schema_editor, from_state, to_state
    ):  # noqa: D102
        pass
