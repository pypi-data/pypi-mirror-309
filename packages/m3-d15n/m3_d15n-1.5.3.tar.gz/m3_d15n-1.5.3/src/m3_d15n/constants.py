# coding: utf-8
from __future__ import unicode_literals


#: Имя схемы в БД для хранения объектов, используемых при деперсонализации.
CORE_SCHEMA = 'd15n_core'

#: Имя схемы в БД для хранения представлений с деперсонализированными данными.
DATA_SCHEMA = 'd15n_data'

#: Имя функции PostgreSQL для деперсонализации имен.
#:
#: Следующие параметры определяют правила деперсонализации:
#:
#:     - :attr:`~m3_d15n.utils.DatabaseParams.visible_chars_begin` ---
#:       количество видимых символов в начале строки (по умолчанию 2).
#:     - :attr:`~m3_d15n.utils.DatabaseParams.visible_chars_end` --- количество
#:       видимых символов в концестроки (по умолчанию 0).
#:     - :attr:`~m3_d15n.utils.DatabaseParams.fill_char` --- символ заполнитель
#:       (по умолчанию \*).
#:     - :attr:`~m3_d15n.utils.DatabaseParams.result_length` --- длина
#:       результирующей строки (по умолчанию 10). Если равен 0, то
#:       соответствует количеству символов в исходной строке.
#:
#: .. seealso::
#:
#:    :class:`m3_d15n.utils.DatabaseParams`
#:
#: Аргументы функции:
#:
#:     - ``source_value`` --- Исходное значение.
#:     - ``visible_chars_begin`` ---  Количество видимых символов в начале
#:       строки. Если не указан, то используется значение параметра
#:       ``visible_chars_begin``.
#:     - ``visible_chars_end`` ---  Количество видимых символов в начале
#:       строки. Если не указан, то используется значение параметра
#:       ``visible_chars_end``.
#:     - ``fill_char`` ---  Количество видимых символов в начале строки. Если
#:       не указан, то используется значение параметра ``fill_char``.
#:     - ``result_length`` --- Количество видимых символов в начале строки.
#:       Если не указан, то используется значение параметра
#:       ``result_length``.
FUNC_DEPERSONALIZE_NAME = (
    CORE_SCHEMA + '.depersonalize_name'
)

#: Имя функции PostgreSQL для деперсонализации до пустого значения.
#:
#: Для любого значения аргумента возвращает ``NULL``.
FUNC_DEPERSONALIZE_TO_NULL = (
    CORE_SCHEMA + '.depersonalize_to_null'
)

#: Имя функции PostgreSQL для деперсонализации до указанной даты.
#:
#: Для любой даты в аргументе возвращает указанную дату.
FUNC_DEPERSONALIZE_TO_DATE = (
    CORE_SCHEMA + '.depersonalize_to_date'
)

#: Имя функции PostgreSQL для деперсонализации до пустой строки.
#:
#: Для любого значения аргумента возвращает пустую строку.
FUNC_DEPERSONALIZE_TO_EMPTY_STRING = (
    CORE_SCHEMA + '.depersonalize_to_empty_string'
)

#: Имя функции PostgreSQL для деперсонализации для замены символов в строке.
#:
#: Функция заменяет все символы, кроме знаков пунктуации, на указанный символ.
#:
#: Примеры (символ-заменитель: x):
#:
#:   - ``000-000-600 01`` → ``xxx-xxx-xxx xx``
#:   - ``I-СП 123456`` → ``x-xx xxxxxx``
FUNC_DEPERSONALIZE_NON_PUNCTUATION = (
    CORE_SCHEMA + '.depersonalize_non_punctuation'
)

#: Префикс URL-адреса.
#:
#: На этом адресе принимаются запросы, которые будут обрабатываться в режиме
#: деперсонализации.
URL_PREFIX = '/d15n'
