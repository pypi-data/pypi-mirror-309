# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations

from m3_d15n import d15n_managers_registry
from m3_d15n import migrations as local_package


def _install(apps, schema_editor):
    if (
        not local_package.always_installed and
        schema_editor.connection.alias in d15n_managers_registry
    ):
        manager = d15n_managers_registry.get(schema_editor.connection.alias)
        manager.install()

        local_package.always_installed = True


def _uninstall(apps, schema_editor):
    if (
        not local_package.always_uninstalled and
        schema_editor.connection.alias in d15n_managers_registry
    ):
        manager = d15n_managers_registry.get(schema_editor.connection.alias)
        manager.uninstall()

        local_package.always_uninstalled = True


class Migration(migrations.Migration):

    """Установка/удаление объектов подсистемы деперсонализации.

    .. seealso::

       :meth:`m3_d15n.utils.D15nManager.install`,
       :meth:`m3_d15n.utils.D15nManager.uninstall`.
    """

    dependencies = []

    operations = [
        local_package.PermanentHStoreExtension(),
        migrations.RunPython(
            code=_install,
            reverse_code=_uninstall,
        ),
    ]
