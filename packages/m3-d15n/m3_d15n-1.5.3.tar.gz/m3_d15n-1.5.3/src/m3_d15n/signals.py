# coding: utf-8
from django.dispatch.dispatcher import Signal


#: Сигнал, отправляемый перед установкой подсистемы в БД.
#:
#: :param sender: класс менеджера базы данных.
#: :type sender: type
#:
#: :param instance: менеджер базы данных.
#: :type instance: m3_d15n.utils.DatabaseManager
#:
#: :param alias: алиас базы данных.
#: :type alias: str
pre_install = Signal()


#: Сигнал, отправляемый после установки подсистемы в БД.
#:
#: :param sender: класс менеджера базы данных.
#: :type sender: type
#:
#: :param instance: менеджер базы данных.
#: :type instance: m3_d15n.utils.DatabaseManager
#:
#: :param alias: алиас базы данных.
#: :type alias: str
post_install = Signal()


#: Сигнал, отправляемый перед удалением подсистемы из БД.
#:
#: :param sender: класс менеджера базы данных.
#: :type sender: type
#:
#: :param instance: менеджер базы данных.
#: :type instance: m3_d15n.utils.DatabaseManager
#:
#: :param alias: алиас базы данных.
#: :type alias: str
pre_uninstall = Signal()


#: Сигнал, отправляемый после удаления подсистемы из БД.
#:
#: :param sender: класс менеджера базы данных.
#: :type sender: type
#:
#: :param instance: менеджер базы данных.
#: :type instance: m3_d15n.utils.DatabaseManager
#:
#: :param alias: алиас базы данных.
#: :type alias: str
post_uninstall = Signal()


#: Сигнал, отправляемый перед включением деперсонализации поля модели.
#:
#: :param sender: класс менеджера деперсонализируемых полей.
#: :type sender: type
#:
#: :param instance: менеджер деперсонализируемых полей.
#: :type instance: m3_d15n.utils.FieldsManager
#:
#: :param field: поле модели, добавляемое в конфигурацию подсистемы
#:     деперсонализации.
#: :type field: django.db.models.field.Field
#:
#: :param function_name: имя деперсонализирующей функции (указывается вместе со
#:     схемой в формате ``'schema.table'``
#: :type function_name: str
#:
#: :param function_params: строка с параметрами деперсонализирующей функции
#: :type function_params: str
pre_add_field = Signal()


#: Сигнал, отправляемый после включением деперсонализации поля модели.
#:
#: :param sender: класс менеджера деперсонализируемых полей.
#: :type sender: type
#:
#: :param instance: менеджер деперсонализируемых полей.
#: :type instance: m3_d15n.utils.FieldsManager
#:
#: :param field: поле модели, добавленное в конфигурацию подсистемы
#:     деперсонализации.
#: :type field: django.db.models.field.Field
#:
#: :param function_name: имя деперсонализирующей функции (указывается вместе со
#:     схемой в формате ``'schema.table'``
#: :type function_name: str
#:
#: :param function_params: строка с параметрами деперсонализирующей функции
#: :type function_params: str
post_add_field = Signal()


#: Сигнал, отправляемый перед выключением деперсонализации поля модели.
#:
#: :param sender: класс менеджера деперсонализируемых полей.
#: :type sender: type
#:
#: :param instance: менеджер деперсонализируемых полей.
#: :type instance: m3_d15n.utils.FieldsManager
#:
#: :param field: поле модели, подлежащее удалению из конфигурации подсистемы
#:     деперсонализации.
#: :type field: django.db.models.field.Field
pre_delete_field = Signal()


#: Сигнал, отправляемый после выключением деперсонализации поля модели.
#:
#: :param sender: класс менеджера деперсонализируемых полей.
#: :type sender: type
#:
#: :param instance: менеджер деперсонализируемых полей.
#: :type instance: m3_d15n.utils.FieldsManager
#:
#: :param field: поле модели, удаленное из конфигурации подсистемы
#:     деперсонализации.
#: :type field: django.db.models.field.Field
post_delete_field = Signal()


#: Сигнал, отправляемый перед переключением режима деперсонализации в БД.
#:
#: :param sender: класс менеджера режима деперсонализации
#: :type sender: type
#:
#: :param instance: менеджер режима деперсонализации.
#: :type instance: m3_d15n.utils.ModeManager
#:
#: :param alias: алиас базы данных.
#: :type alias: str
#:
#: :param mode: флаг, указывающий на включение (``True``), либо отключение
#:     (``False``) режима деперсонализации.
#: :type mode: bool
pre_switch_mode = Signal()


#: Сигнал, отправляемый после переключением режима деперсонализации в БД.
#:
#: :param sender: класс менеджера режима деперсонализации
#: :type sender: type
#:
#: :param instance: менеджер режима деперсонализации.
#: :type instance: m3_d15n.utils.ModeManager
#:
#: :param alias: алиас базы данных.
#: :type alias: str
#:
#: :param mode: флаг, указывающий на включение (``True``), либо отключение
#:     (``False``) режима деперсонализации.
#: :type mode: bool
post_switch_mode = Signal()
