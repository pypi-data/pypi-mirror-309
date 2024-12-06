-------------------------------------------------------------------------------
-- Т.к. содержимое данного файла прогоняется через метод format строки Python,
-- фигурные скобки указывают на места подстановки параметров. Поэтом при
-- необходимости использования фигурных скобок, используйте двойные скобки,
-- т.к. метод format заменит их на одинарные.
-------------------------------------------------------------------------------

drop trigger if exists set_column_number on {core_schema}.columns_config;
drop event trigger if exists objects_dropped;
drop trigger if exists columns_config_changed on {core_schema}.columns_config;
drop event trigger if exists ddl_command_ended;

drop trigger if exists
    {core_schema}_set_column_number
    on {core_schema}.columns_config;
drop event trigger if exists
    {core_schema}_objects_dropped;
drop trigger if exists
    {core_schema}_columns_config_changed
    on {core_schema}.columns_config;
drop event trigger if exists
    {core_schema}_ddl_command_ended;
-------------------------------------------------------------------------------

create schema if not exists {core_schema};
comment
    on schema {core_schema}
    is 'Код, реализующий деперсонализацию данных';

create schema if not exists {data_schema};
comment
    on schema {data_schema}
    is 'Представления, деперсонализирующие данные основной БД';
-------------------------------------------------------------------------------

create or replace function {core_schema}.drop_functions_by_name(
    function_name name,
    function_schema name default '{core_schema}'
)
returns void
as $body$
    ---------------------------------------------------------------------------
    -- Удаляет все функции с указанным именем в схеме {core_schema}
    -- вне зависимости от типа и количества аргументов.
    --
    -- Аргументы:
    --     function_name
    --         Имя удаляемых функций.
    --     function_schema
    --         Схема, в которой расположены удаляемые функции.
    ---------------------------------------------------------------------------
    declare
        rec record;
        sql text;
    begin
        for rec in
            select
                pg_proc.oid as func_oid,
                pg_namespace.nspname as func_schema,
                pg_proc.proname as func_name
            from
                pg_proc
                inner join pg_namespace on (
                    pg_proc.pronamespace = pg_namespace.oid
                )
            where
                pg_namespace.nspname = function_schema and
                pg_proc.proname = function_name
        loop
            execute
                format(
                    'drop function %I.%I(%s) cascade',
                    rec.func_schema,
                    rec.func_name,
                    pg_get_function_identity_arguments(rec.func_oid)
                );
        end loop;
 end;
$body$
language plpgsql
volatile;


select {core_schema}.drop_functions_by_name('get_param');
select {core_schema}.drop_functions_by_name('depersonalize_name');
select {core_schema}.drop_functions_by_name('depersonalize_to_null');
select {core_schema}.drop_functions_by_name('depersonalize_to_date');
select {core_schema}.drop_functions_by_name('depersonalize_to_empty_string');
select {core_schema}.drop_functions_by_name('depersonalize_non_punctuation');
select {core_schema}.drop_functions_by_name('depersonalize_year');
select {core_schema}.drop_functions_by_name('set_column_number');
select {core_schema}.drop_functions_by_name('on_columns_config_changed');
select {core_schema}.drop_functions_by_name('on_ddl_command_end');
select {core_schema}.drop_functions_by_name('on_sql_drop');
select {core_schema}.drop_functions_by_name('get_table_columns');
select {core_schema}.drop_functions_by_name('get_column_params');
select {core_schema}.drop_functions_by_name('overwrite_columns');
select {core_schema}.drop_functions_by_name('get_columns_values');
select {core_schema}.drop_functions_by_name('get_equal_expressions');
select {core_schema}.drop_functions_by_name('get_table_schema');
select {core_schema}.drop_functions_by_name('get_column_default_expression');
select {core_schema}.drop_functions_by_name('on_d15n_view_insert');
select {core_schema}.drop_functions_by_name('on_d15n_view_update');
select {core_schema}.drop_functions_by_name('create_view_for_table');
select {core_schema}.drop_functions_by_name('update_views_set');
-------------------------------------------------------------------------------

create function {core_schema}.get_param(
    param_name text,
    default_value text default null
)
returns text
as $body$
    ---------------------------------------------------------------------------
    -- Возвращает значение параметра конфигурации.
    --
    -- Аргументы:
    --     param_name
    --         Имя параметра конфигурации.
    --     default_value
    --         Значение по умолчанию. Возвращается в случае, если значение
    --         указанного параметра не устанавливалось ранее.
    ---------------------------------------------------------------------------
    declare
        result text;
    begin
        result := current_setting(param_name);
        if result is null or result = '' then
            result := default_value;
        end if;

        return result;
    exception
        when others then
            return default_value;
    end;
$body$
LANGUAGE plpgsql;
-------------------------------------------------------------------------------

create function {core_schema}.depersonalize_name(
    source_value text,
    visible_chars_begin int default null,
    visible_chars_end int default null,
    fill_char text default null,
    result_length int default null
)
returns text
as $body$
    ---------------------------------------------------------------------------
    -- Выполняет деперсонализацию имен.
    --
    -- Следующие параметры определяют правила деперсонализации:
    --     * {core_schema}.dn_visible_chars_begin - количество видимых символов в
    --       начале строки (по умолчанию 2).
    --     * {core_schema}.dn_visible_chars_end - количество видимых символов в
    --       конце строки (по умолчанию 0).
    --     * {core_schema}.dn_fill_char - символ заполнитель (по умолчанию *).
    --     * {core_schema}.dn_result_length - длина результирующей строки (по
    --       умолчанию 10). Если равен 0, то соответствует количеству символов
    --       в исходной строке.
    --
    -- Аргументы:
    --     source_value
    --         Исходное значение.
    --     visible_chars_begin
    --         Количество видимых символов в начале строки. Если не указан, то
    --         используется значение параметра
    --         {core_schema}.dn_visible_chars_begin
    --     visible_chars_end
    --         Количество видимых символов в начале строки. Если не указан, то
    --         используется значение параметра
    --         {core_schema}.visible_chars_end
    --     fill_char
    --         Количество видимых символов в начале строки. Если не указан, то
    --         используется значение параметра
    --         {core_schema}.fill_char
    --     result_length
    --         Количество видимых символов в начале строки. Если не указан, то
    --         используется значение параметра
    --         {core_schema}.result_length
    ---------------------------------------------------------------------------
    declare
        _visible_chars_begin int;
        _visible_chars_end int;
        _fill_char text;
        _result_length int;
        n int;

        prefix text;
        filler text;
        suffix text;
    begin
        if source_value is null or length(source_value) = 0 then
            return source_value;
        end if;

        _visible_chars_begin := greatest(0::int, coalesce(
            visible_chars_begin,
            {core_schema}.get_param(
                '{core_schema}.dn_visible_chars_begin', '2'
            )::int
        ));
        _visible_chars_end := greatest(0::int, coalesce(
            visible_chars_end,
            {core_schema}.get_param(
                '{core_schema}.dn_visible_chars_end', '0'
            )::int
        ));
        _result_length := greatest(0::int, coalesce(
            result_length,
            {core_schema}.get_param(
                '{core_schema}.dn_result_length', '10'
            )::int
        ));
        _fill_char := coalesce(
            fill_char,
            {core_schema}.get_param(
                '{core_schema}.dn_fill_char', '*'
            )::text
        );

        prefix := substring(source_value for _visible_chars_begin);

        suffix := substring(
            source_value
            from greatest(
                _visible_chars_begin + 1,
                length(source_value) - _visible_chars_end + 1
            )
            for _visible_chars_end
        );

        if _result_length = 0 then
            _result_length := length(source_value);
            if _result_length - length(prefix) - length(suffix) = 0 then
                suffix := repeat(_fill_char, length(suffix));
            end if;
        end if;
        filler := repeat(
            _fill_char, _result_length - length(prefix) - length(suffix)
        );

        return prefix || filler || suffix;
    end;
$body$
language plpgsql
immutable;
-------------------------------------------------------------------------------

create function {core_schema}.depersonalize_to_null(
    source_value anyelement,
    out result anyelement
)
as $body$
    ---------------------------------------------------------------------------
    -- Функция деперсонализации данных: заменяет любое значение любого типа
    -- на null. null будет возвращен того же типа, что и исходное значение.
    --
    -- Аргументы:
    --     source_value
    --         Исходное значение.
    ---------------------------------------------------------------------------
    begin
      result := null;
    end;
$body$
language plpgsql
immutable;
-------------------------------------------------------------------------------

create function {core_schema}.depersonalize_to_date(
    source_value date,
    result date
)
returns date
as $body$
    ---------------------------------------------------------------------------
    -- Функция деперсонализации данных: заменяет любое значение на указанную
    -- дату.
    --
    -- Аргументы:
    --     source_value
    --         Исходное значение.
    ---------------------------------------------------------------------------
    select
        case
            when result is null then null
            else result
        end;
$body$
language sql
immutable;
-------------------------------------------------------------------------------

create function {core_schema}.depersonalize_to_empty_string(
    source_value text
)
returns text
as $body$
    ---------------------------------------------------------------------------
    -- Функция деперсонализации данных: заменяет любое значение на пустую
    -- строку.
    --
    -- Аргументы:
    --     source_value
    --         Исходное значение.
    ---------------------------------------------------------------------------
    select
        case
            when source_value is null then null
            else ''::text
        end;
$body$
language sql
immutable;
-------------------------------------------------------------------------------

create function {core_schema}.depersonalize_non_punctuation(
    source_value text,
    replace_char char
)
returns text
as $body$
    ---------------------------------------------------------------------------
    -- Функция деперсонализации данных: заменяет все символы в строке, кроме
    -- знаков пунктуации, на указанный символ.
    --
    -- Аргументы:
    --     source_value
    --         Исходное значение.
    --     replace_char
    --         Символ-заменитель.
    ---------------------------------------------------------------------------
    select case
        when source_value is null or length(source_value) = 0 then source_value
        else array_to_string(
            array(
                select
                    case
                        when position(
                            ch in ' ~`!@#$%^&*()-_=+[{}]''"\|/.,<>;:'
                        )::boolean then ch
                    else
                        replace_char
                    end
                from
                    unnest(string_to_array(source_value, null)) as t(ch)
            ),
            ''
        )
    end;
$body$
language sql
immutable;
-------------------------------------------------------------------------------

create function {core_schema}.depersonalize_year(
    source_value date,
    new_value int
)
returns date
as $body$
    ---------------------------------------------------------------------------
    -- Функция деперсонализации данных: заменяет год в дате на указанный.
    --
    -- Аргументы:
    --     source_value
    --         Исходное значение.
    --     new_value
    --         Новое значение года в дате.
    ---------------------------------------------------------------------------
    select case
        when source_value is null then null
        else make_date(
            new_value,
            extract('month' from source_value)::int,
            extract('day' from source_value)::int
        )
    end;
$body$
language sql
immutable;
-------------------------------------------------------------------------------

-- Столбцы, подлежащие деперсонализации.
create table if not exists {core_schema}.columns_config
(
    table_oid oid not null,
    column_name name not null,
    column_number smallint not null,
    function_oid oid not null,
    function_params text not null default '',
    unique (table_oid, column_name),
    unique (table_oid, column_number)
);
comment
    on table {core_schema}.columns_config
    is 'Столбцы в таблицах основной БД, подлежащие деперсонализации';
-------------------------------------------------------------------------------

create function {core_schema}.set_column_number()
returns trigger
as $body$
    ---------------------------------------------------------------------------
    -- Заполняет поле column_number в таблице {core_schema}.columns_config
    -- при добавлении и изменении записей.
    ---------------------------------------------------------------------------
    begin
        -- Заполнение поля column_number.
        select
            attnum
        into
            NEW.column_number
        from
            pg_catalog.pg_attribute
        where
            attrelid = NEW.table_oid and
            attname = NEW.column_name;

        return NEW;
    end;
$body$
language plpgsql
volatile;
-------------------------------------------------------------------------------

create function {core_schema}.on_columns_config_changed()
returns trigger
as $body$
    ---------------------------------------------------------------------------
    -- Создает представление с деперсонализированными данными при добавлении
    -- записей в таблицу {core_schema}.columns_config.
    ---------------------------------------------------------------------------
    declare
        rec record;
        c int;
    begin
        perform {core_schema}.update_views_set();

        return NEW;
    end;
$body$
language plpgsql
volatile;
-------------------------------------------------------------------------------

create function {core_schema}.on_ddl_command_end()
returns event_trigger
as $body$
    ---------------------------------------------------------------------------
    -- При переименовании столбца обновляет запись в columns_config.
    ---------------------------------------------------------------------------
    declare
        in_migration boolean;
        info record;
        config_column_name name;
        new_column_name name;
    begin
        if TG_TAG = 'ALTER TABLE' then
            in_migration := {core_schema}.get_param(
                '{core_schema}.in_migration', ''
            ) = 'TRUE';

            for info in select * from pg_event_trigger_ddl_commands()
            loop
                if info.object_type = 'table column' then
                    select column_name into config_column_name
                    from {core_schema}.columns_config
                    where
                        table_oid = info.objid and
                        column_number = info.objsubid;

                    if config_column_name is not null then
                        new_column_name := (string_to_array(
                            info.object_identity, '.'
                        ))[3];
                        if config_column_name <> new_column_name then
                            -- Колонка была переименована.
                            if in_migration then
                                alter table {core_schema}.columns_config
                                    disable trigger
                                    {core_schema}_columns_config_changed;
                            end if;

                            execute format(
                                'update {core_schema}.columns_config set '
                                'column_name = %L '
                                'where table_oid = %s and column_number = %s',
                                new_column_name,
                                info.objid,
                                info.objsubid
                            );

                            if in_migration then
                                alter table {core_schema}.columns_config
                                    enable trigger
                                    {core_schema}_columns_config_changed;
                            end if;
                        end if;
                    end if;
                end if;
            end loop;
        end if;
    end;
$body$
language plpgsql;
-------------------------------------------------------------------------------

create function {core_schema}.on_sql_drop()
returns event_trigger
as $body$
    ---------------------------------------------------------------------------
    -- При удалении таблицы из БД удаляет соответствующие записи из
    -- таблицы columns_config.
    ---------------------------------------------------------------------------
    declare
        in_migration boolean;
        object_info record;
    begin
        in_migration := {core_schema}.get_param(
            '{core_schema}.in_migration', ''
        ) = 'TRUE';

        for object_info in select * from pg_event_trigger_dropped_objects()
        loop
            if TG_TAG = 'DROP TABLE' then
                -- Отключение триггера columns_config_changed нужно для того,
                -- чтобы не создавались деперсонализирующие представления
                -- (на время выполнения миграций они удаляются).
                if in_migration then
                    alter table {core_schema}.columns_config
                        disable trigger {core_schema}_columns_config_changed;
                end if;

                execute format(
                    'delete '
                    'from {core_schema}.columns_config '
                    'where table_oid = %s',
                    object_info.objid
                );

                if in_migration then
                    alter table {core_schema}.columns_config
                        enable trigger {core_schema}_columns_config_changed;
                end if;
            elsif (
                TG_TAG = 'ALTER TABLE' and
                object_info.object_type = 'table column'
            ) then
                -- Отключение триггера columns_config_changed нужно для того,
                -- чтобы не создавались деперсонализирующие представления
                -- (на время выполнения миграций они удаляются).
                if in_migration then
                    alter table {core_schema}.columns_config
                        disable trigger {core_schema}_columns_config_changed;
                end if;

                execute format(
                    'delete '
                    'from {core_schema}.columns_config '
                    'where table_oid = %s and column_name = %L',
                    object_info.objid,
                    (string_to_array(object_info.object_identity, '.'))[3]
                );

                if in_migration then
                    alter table {core_schema}.columns_config
                        enable trigger {core_schema}_columns_config_changed;
                end if;
            end if;
        end loop;
    end;
$body$
language plpgsql;
-------------------------------------------------------------------------------

create or replace view {core_schema}.columns_config_as_names as
select
    table_schemas.nspname as table_schema,
    tables.relname as table_name,
    configs.column_name as column_name,
    function_schemas.nspname as function_schema,
    functions.proname as function_name,
    configs.function_params as function_params
from
    {core_schema}.columns_config configs
    inner join pg_catalog.pg_class tables on (
        configs.table_oid = tables.oid
    )
    inner join pg_catalog.pg_namespace table_schemas on (
        tables.relnamespace = table_schemas.oid
    )
    inner join pg_catalog.pg_proc functions on (
        configs.function_oid = functions.oid
    )
    inner join pg_catalog.pg_namespace function_schemas on (
        functions.pronamespace = function_schemas.oid
    );
-------------------------------------------------------------------------------

create function {core_schema}.get_table_columns(
    table_schema name,
    table_name name,
    primary_key boolean default null,
    quote boolean default false
)
returns text[]
as $body$
    ---------------------------------------------------------------------------
    -- Возвращает имена столбцов и их типы указанной таблицы.
    --
    -- В результирующем массиве имена полей и их типы чередуются: нечетные
    -- элементы содержат имена полей, а четные - типы данных.
    --
    -- Аргументы:
    --     table_schema
    --         Схема таблицы.
    --     table_name
    --         Имя таблицы.
    --     primary_key
    --         Флаг, определяющий то, какие столбцы таблицы будут включены в
    --         результат (null - все столбцы, false - все, кроме столбцов
    --         входящих в первичный ключ, true - столбцы, входящие в первичный
    --         ключ).
    --     quote
    --         Флаг, определяющий, нужно ли выполнять для имен столбцов функцию
    --         quote_ident().
    ---------------------------------------------------------------------------
    declare
        result text[] = '{}';
        rec record;
    begin
        for rec in
            select
                case
                    when quote then quote_ident(columns.attname)
                    else columns.attname::text
                end as column_name,
                format_type(columns.atttypid, columns.atttypmod) as column_type
            from
                pg_catalog.pg_attribute columns
                left join pg_catalog.pg_index indexes on (
                    indexes.indisprimary and
                    columns.attrelid = indexes.indrelid
                )
            where
                columns.attrelid = format(
                    '%I.%I', table_schema, table_name
                )::regclass::oid and
                columns.attisdropped = false and
                columns.attnum >= 1 and
                case
                    when primary_key is null then
                        true
                    when primary_key then
                        indexes.indkey is not null and
                        columns.attnum = any(indexes.indkey)
                    else
                        indexes.indkey is null or
                        columns.attnum <> any(indexes.indkey)
                end
            order by
                columns.attnum
        loop
            result := result || rec.column_name || rec.column_type;
        end loop;

        return result;
    end;
$body$
language plpgsql
immutable;
-------------------------------------------------------------------------------

create function {core_schema}.get_column_params(
    table_columns text[],
    param int,
    quote boolean default false
)
returns text[]
as $body$
    ---------------------------------------------------------------------------
    -- Возвращает имена столбцов из массива с именами и типами столбцов.
    --
    -- Аргументы:
    --     table_columns
    --         Массив с именами и типами столбцов. В нечетных позициях должны
    --         быть имена столбцов, а в четных - их типы данных.
    --     param
    --         1 - имена столбцов, 0 - типы данных столбцов.
    --     quote
    --         Флаг, определяющий, нужно ли выполнять для имен столбцов функцию
    --         quote_ident().
    ---------------------------------------------------------------------------
    declare
        result text[];
        i int;
        value text;
    begin
        if array_length(table_columns, 1) > 0 then
            for i in 1..(array_length(table_columns, 1) / 2)
            loop
                value := table_columns[i * 2 - param];
                if quote then
                    value := quote_ident(value);
                end if;

                result := result || value;
            end loop;
        end if;

        return result;
    end;
$body$
language plpgsql
immutable;
-------------------------------------------------------------------------------

create function {core_schema}.overwrite_columns(
    tbl_schema name,
    tbl_name name,
    tbl_columns text[]
)
returns text[]
as $body$
    ---------------------------------------------------------------------------
    -- Заменяет столбцы таблицы, подлежащие деперсонализации, на вызовы
    -- деперсонализирующих функций.
    --
    -- Аргументы:
    --     tbl_schema
    --         Имя схемы таблицы.
    --     tbl_name
    --         Имя таблицы.
    --     tbl_columns
    --         Массив с именами и типами данных колонок таблицы.
    ---------------------------------------------------------------------------
    declare
        columns text[] := '{}';  -- столбцы, подлежащие деперсонализации.
        functions text[] := '{}';  -- деперсонализирующие функции.
        params text[] := '{}'; -- параметры функции.
        result text[] := '{}';
        rec record;
        col_name text;
        col_type text;
        position int;
        i int;
    begin
        -- Загрузка параметров деперсонализации для указанной таблицы.
        for rec in
            select
                column_name,
                function_schema,
                function_name,
                function_params
            from
                {core_schema}.columns_config_as_names
            where
                table_schema = tbl_schema and
                table_name = tbl_name
        loop
            columns := columns || rec.column_name::text;
            functions := functions || format(
                '%I.%I', rec.function_schema, rec.function_name
            );
            params := params || rec.function_params;
        end loop;

        -- Замена столбцов на вызовы деперсонализирующих функций.
        for i in 1..(array_length(tbl_columns, 1) / 2)
        loop
            col_name := tbl_columns[i * 2 - 1];
            col_type := tbl_columns[i * 2];
            position := array_position(columns, col_name);
            if position is null then
                -- В параметрах деперсонализации столбец col_name не указано,
                -- поэтому добавляем его в представление как есть.
                result := array_append(result, format('%I', col_name));
            else
                -- Cтолбец col_name указан в параметрах деперсонализации,
                -- поэтому вместо значений этого столбца указываем вызов
                -- деперсонализирующей функции со значением данного столбца в
                -- качестве аргумента.
                result := array_append(result,
                    format(
                        '%s(%I%s)::%s as %I',
                        functions[position],
                        col_name,
                        case
                            when params[position] = '' then ''
                            else ', ' || params[position]
                        end,
                        col_type,
                        col_name
                    )
                );
            end if;
        end loop;

        return result;
    end;
$body$
language plpgsql
immutable;
-------------------------------------------------------------------------------

create function {core_schema}.get_columns_values(
    table_schema name,
    table_name name,
    rec anyelement,
    table_columns text[]
)
returns text[]
as $body$
    ---------------------------------------------------------------------------
    -- Возвращает значения указанных столбцов записи таблицы.
    --
    -- Аргументы:
    --     table_schema
    --         Имя схемы таблицы.
    --     table_name
    --         Имя таблицы.
    --     rec
    --         Запись таблицы, из которой извлекаются значения .
    --     table_columns
    --         Имена и типы данных столбцов.
    ---------------------------------------------------------------------------
    declare
        column_name text;
        column_type text;
        column_value text;
        result text[] = '{}';
        i int;
    begin
        if array_length(table_columns, 1) > 0 then
            for i in 1..(array_length(table_columns, 1) / 2)
            loop
                -- Двумерный массив table_columns на самом деле
                -- преобразовывается в одномерный :(
                column_name := table_columns[i * 2 - 1];
                column_type := table_columns[i * 2];

                execute
                    format(
                        'select ($1::%I.%I).%s::text',
                        table_schema,
                        table_name,
                        column_name
                    )
                    into column_value
                    using rec;

                result := result || (
                    quote_literal(column_value) || '::' || column_type
                );
            end loop;
        end if;

        return result;
    end;
$body$
language plpgsql
volatile;
-------------------------------------------------------------------------------

create function {core_schema}.get_equal_expressions(
    table_schema name,
    table_name name,
    rec anyelement,
    table_columns text[],
    use_is_for_null boolean
)
returns text[]
as $body$
    ---------------------------------------------------------------------------
    -- Возвращает массив из строк вида 'column_name = column_value'.
    --
    -- Аргументы:
    --     table_schema
    --         Имя схемы таблицы.
    --     table_name
    --         Имя таблицы.
    --     rec
    --         Запись таблицы, из которой извлекаются значения.
    --     table_columns
    --         Имена и типы данных столбцов.
    --     use_is_for_null
    --         Флаг, определяющий необходимость использования is для значений
    --         null.
    ---------------------------------------------------------------------------
    select array(
        select
            case
                when column_value is null then
                    format(
                        '%I %s NULL',
                        column_name,
                        case when use_is_for_null then 'is' else '=' end
                    )
                else
                    format('%I = %s', column_name, column_value)
            end
        from
            unnest(
                {core_schema}.get_column_params(table_columns, 1),
                {core_schema}.get_columns_values(
                    table_schema, table_name, rec, table_columns
                )
            ) as t(column_name, column_value)
    );
$body$
language sql
volatile;
-------------------------------------------------------------------------------

create function {core_schema}.get_table_schema(
    table_name name
)
returns text
as $body$
    ---------------------------------------------------------------------------
    -- Возвращает схему, в которой была найдена таблица table_name.
    --
    -- Аргументы:
    --     table_name
    --         Имя таблицы для поиска.
    ---------------------------------------------------------------------------
    select
        s
    from
        unnest(
            string_to_array(current_setting('search_path'), ', ')
        ) as t(s)
    where
        s <> '{data_schema}' and
        exists(
            select
                1
            from
                pg_catalog.pg_tables
            where
                schemaname = case
                    when s = '"$user"' then current_user
                    else s
                end and
                tablename = table_name
        );
$body$
language sql
immutable;
-------------------------------------------------------------------------------

create or replace function {core_schema}.get_column_default_expression(
    schema_name name,
    table_name name,
    column_name name
)
returns text
as $body$
    ---------------------------------------------------------------------------
    -- Возвращает значение по умолчанию для поля таблицы.
    --
    -- Аргументы:
    --     table_name
    --         Имя таблицы.
    --     column_name
    --         Имя столбца.
    ---------------------------------------------------------------------------
    declare
        default_expression text;
        result text;
    begin
        select
            d.adsrc
        into
            default_expression
        from
            pg_catalog.pg_attribute a
            left join pg_catalog.pg_attrdef d ON (
                a.attrelid = d.adrelid and a.attnum = d.adnum
            )
        where
            not a.attisdropped and
            a.attnum > 0 and
            a.attrelid = (schema_name || '.' || table_name)::regclass and
            a.attname = column_name;

        if default_expression is not null then
            execute
                'select ' || default_expression
                into result;
        else
            result := null;
        end if;

        return result;
    end;
$body$
language plpgsql
volatile;
-------------------------------------------------------------------------------
create or replace function update_fields(r anyelement, variadic changes text[])
returns anyelement as $$
select $1 #= hstore($2);
$$ language sql;

create function {core_schema}.on_d15n_view_insert()
returns trigger
as $body$
    ---------------------------------------------------------------------------
    -- Обеспечивает вставку записи деперсонализированную таблицу через
    -- деперсонализирующее представление.
    ---------------------------------------------------------------------------
    declare
        column_name name;
        column_type text;
        column_value text;
        table_columns text[];
        column_values text[];
        pk_table_columns text[];
        pk_column_values text[];
        has_pk boolean;
        table_schema name;
        rec record;
        i int;
    begin
        table_schema := {core_schema}.get_table_schema(TG_TABLE_NAME);
        if table_schema is null then
            raise exception 'Table "%" not found', TG_TABLE_NAME;
        end if;

        -- Значения колонок, не входящих в первичный ключ.
        table_columns := {core_schema}.get_table_columns(
            table_schema, TG_TABLE_NAME, false, false
        );
        column_values := {core_schema}.get_columns_values(
            TG_TABLE_SCHEMA, TG_TABLE_NAME, NEW, table_columns
        );

        -- Значения колонок, входящих в первичный ключ.
        pk_table_columns := {core_schema}.get_table_columns(
           table_schema, TG_TABLE_NAME, true, false
        );
        pk_column_values := {core_schema}.get_columns_values(
            TG_TABLE_SCHEMA, TG_TABLE_NAME, NEW, pk_table_columns
        );

        -- Заполнение пустых столбцов из первичного ключа значениями по
        -- умолчанию (обычно это следующий элемент последовательности).
        -- Необходимость делать это вручную обусловлена тем, что у
        -- непривилегированного пользователя нет прав на чтение из таблицы и
        -- поэтому нет возможности использовать параметр returning оператора
        -- insert, чтобы получить значение ключевых полей созданной записи.
        i := 1;
        foreach column_value in array pk_column_values loop
            column_name := pk_table_columns[i * 2 - 1];
            column_type := pk_table_columns[i * 2];

            if column_value is null then
                column_value := {core_schema}.get_column_default_expression(
                    table_schema, TG_TABLE_NAME, column_name
                );
                if column_value is not null then
                    NEW = NEW #= hstore(column_name, column_value);
                    table_columns := array_prepend(
                        column_type::text, table_columns
                    );
                    table_columns := array_prepend(
                        column_name::text, table_columns
                    );
                    column_values := array_prepend(
                        column_value, column_values
                    );
                end if;
            end if;

            i := i + 1;
        end loop;

        -- Добавление записи в таблицу.
        execute format(
            'insert into %I.%I (%s) values (%s)',
            table_schema,
            TG_TABLE_NAME,
            array_to_string(
                {core_schema}.get_column_params(table_columns, 1, true),
                ', '
            ),
            array_to_string(column_values, ', ', 'null')
        );

        return NEW;
    end;
$body$
language plpgsql
volatile;
-------------------------------------------------------------------------------

create function {core_schema}.on_d15n_view_update()
returns trigger
as $body$
    ---------------------------------------------------------------------------
    -- Обеспечивает изменение записи в деперсонализированной таблице через
    -- деперсонализирующее представление. Деперсонализированные столбцы
    -- остаются без изменения.
    ---------------------------------------------------------------------------
    declare
        d15n_column_names text[];
        set_column_names text[] = '{}';
        set_column_types text[] = '{}';
        set_columns text[];
        set_expressions text[];
        where_columns text[];
        where_expressions text[];
        tbl_schema text;
        col_name text;
        i int;
    begin
        tbl_schema := {core_schema}.get_table_schema(TG_TABLE_NAME);
        if tbl_schema is null then
            raise exception 'Table "%" not found', TG_TABLE_NAME;
        end if;

        -- Загрузка деперсонализированных полей таблицы.
        d15n_column_names := array(
            select
                column_name
            from
                {core_schema}.columns_config_as_names
            where
                table_schema = tbl_schema and
                table_name = TG_TABLE_NAME
        );

        set_columns := {core_schema}.get_table_columns(
            tbl_schema, TG_TABLE_NAME, false, false
        );
        -- Исключение деперсонализированных полей из раздела SET команды UPDATE
        if array_length(set_columns, 1) > 0 then
            for i in 1..(array_length(set_columns, 1) / 2) loop
                col_name := set_columns[i * 2 - 1];
                if array_position(d15n_column_names, col_name) is null then
                    set_column_names := set_column_names || col_name;
                    set_column_types := set_column_types || set_columns[i * 2];
                end if;
            end loop;
        end if;

        set_columns := '{}';
        if array_length(set_column_names, 1) > 0 then
            for i in 1..array_length(set_column_names, 1) loop
                set_columns := (
                    set_columns ||
                    set_column_names[i] ||
                    set_column_types[i]
                );
            end loop;
        end if;

        set_expressions := {core_schema}.get_equal_expressions(
            TG_TABLE_SCHEMA, TG_TABLE_NAME, NEW, set_columns, false
        );

        where_columns := {core_schema}.get_table_columns(
            tbl_schema::text, TG_TABLE_NAME::text, true, true
        );

        where_expressions := {core_schema}.get_equal_expressions(
            TG_TABLE_SCHEMA::text,
            TG_TABLE_NAME::text,
            NEW,
            where_columns,
            true
        );

        if array_length(set_expressions, 1) > 0 then
            execute
                format(
                    'update %I.%I set %s where %s',
                    tbl_schema,
                    TG_TABLE_NAME,
                    array_to_string(set_expressions, ', '),
                    array_to_string(where_expressions, ', ')
                );
            return NEW;
        else
            return OLD;
        end if;
    end;
$body$
language plpgsql
volatile;
-------------------------------------------------------------------------------

create function {core_schema}.create_view_for_table(
    tbl_schema name,
    tbl_name name
)
returns void
as $body$
    ---------------------------------------------------------------------------
    -- Для таблицы с указанным именем создает деперсонализированное
    -- представление.
    --
    -- Аргументы:
    --     table_schema
    --         Имя схемы таблицы.
    --     table_name
    --         Имя таблицы.
    ---------------------------------------------------------------------------
    declare
        view_columns text[];
    begin
        view_columns := {core_schema}.overwrite_columns(
            tbl_schema,
            tbl_name,
            {core_schema}.get_table_columns(tbl_schema, tbl_name)
        );
        -- Создание деперсонализирующего представления.
        execute
            format(
                'create view %I.%I as '
                'select %s '
                'from %I.%I ',
                '{data_schema}',
                tbl_name,
                array_to_string(view_columns, ', '),
                tbl_schema,
                tbl_name
            );
        -- Подключение обработчика для операций вставки записей (INSERT).
        execute
            format(
                'create trigger d15n_insert '
                'instead of insert '
                'on {data_schema}.%I '
                'for each row '
                'execute procedure {core_schema}.on_d15n_view_insert()',
                tbl_name
            );
        -- Подключение обработчика для операций изменения записей (UPDATE).
        execute
            format(
                'create trigger d15n_update '
                'instead of update '
                'on {data_schema}.%I '
                'for each row '
                'execute procedure {core_schema}.on_d15n_view_update()',
                tbl_name
            );
    end;
$body$
language plpgsql
volatile;
-------------------------------------------------------------------------------

create function {core_schema}.update_views_set()
returns void
as $body$
    ---------------------------------------------------------------------------
    -- Обновляет представления с деперсонализированными данными в соответствии
    -- с конфигурацией подсистемы деперсонализации.
    ---------------------------------------------------------------------------
    declare
        rec record;
    begin
        -- Удаление существующих представлений в схеме {data_schema}.
        for rec in
            select
                tables.relname as table_name
            from
                pg_catalog.pg_class tables
                inner join pg_catalog.pg_namespace schemas on (
                    tables.relnamespace = schemas.oid
                )
            where
                tables.relkind = 'v' and
                schemas.nspname = '{data_schema}'
        loop
            execute
                format(
                    'drop view "{data_schema}"."%s"',
                    rec.table_name
                );
        end loop;

        -- Создание новых представлений в соответствии с конфигурацией.
        for rec in
            select
                distinct table_schema, table_name
            from
                {core_schema}.columns_config_as_names
        loop
            perform {core_schema}.create_view_for_table(
                rec.table_schema, rec.table_name
            );
        end loop;
    end;
$body$
language plpgsql
volatile;
-------------------------------------------------------------------------------

create trigger {core_schema}_set_column_number
    before insert or update
    on {core_schema}.columns_config
    for each row
    execute procedure {core_schema}.set_column_number();

create trigger {core_schema}_columns_config_changed
    after insert or update or delete
    on {core_schema}.columns_config
    for each statement
    execute procedure {core_schema}.on_columns_config_changed();

create event trigger {core_schema}_ddl_command_ended
    on ddl_command_end
    execute procedure {core_schema}.on_ddl_command_end();

create event trigger {core_schema}_objects_dropped
    on sql_drop
    execute procedure {core_schema}.on_sql_drop();
