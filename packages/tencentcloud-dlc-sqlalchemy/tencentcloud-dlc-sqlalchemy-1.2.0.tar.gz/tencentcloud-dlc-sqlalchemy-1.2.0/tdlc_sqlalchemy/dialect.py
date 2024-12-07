import re
from tdlc_connector import constants

import sqlalchemy.types as sqltypes
from sqlalchemy.engine import default, reflection
from sqlalchemy.sql import text


from .base import (
    DlcCompiler,
    DlcDDLCompiler,
    DlcExecutionContext,
    DlcIdentifierPreparer,
    DlcTypeCompiler,
)
from . import types


COMPATIBLE_TYPES = {
    "TINYINT"           :types.TINYINT,
    "SMALLINT"          :types.SMALLINT,
    "BIGINT"            :types.BIGINT,
    "INT"               :types.INT,
    "INTEGER"           :types.INTEGER,
    "FLOAT"             :types.FLOAT,
    "DOUBLE"            :types.DOUBLE,
    "DECIMAL"           :types.DECIMAL,

    "BOOLEAN"           :types.BOOLEAN,
    "CHAR"              :types.CHAR,
    "VARCHAR"           :types.VARCHAR,
    "STRING"            :types.String,
    "TEXT"              :types.TEXT,
    "TINYTEXT"          :types.TEXT,
    "MEDIUMTEXT"        :types.TEXT,
    "LONGTEXT"          :types.TEXT,



    "DATE"              :types.DATE,
    "TIME"              :types.TIME,
    "TIMESTAMP"         :types.TIMESTAMP,
    "DATETIME"          :types.DATETIME,

    "JSON"              :types.JSON,
    "ARRAY"             :types.ARRAY,
    "STRUCT"            :types.STRUCT,
    "MAP"               :types.JSON,

    "BOOL"              :types.BOOLEAN,
    "BOOLEAN"           :types.BOOLEAN,
}

TYPE_REGEXP = r'(\w+)(\((\d+)(.+(\d+))?\))?'
def get_column_type(_type):

    m = re.match(TYPE_REGEXP, _type)

    name = m.group(1).upper()
    arg1 = m.group(3)
    arg2 = m.group(5)

    col_type = COMPATIBLE_TYPES.get(name, sqltypes.NullType)
    col_type_kw = {}

    if name in ('CHAR', 'STRING', 'VARCHAR') and arg1 is not None:
        col_type_kw['length'] = int(arg1)
    
    elif name in ('DECIMAL',) and arg1 is not None and arg2 is None:
        col_type_kw['precision'] = int(arg1)
        col_type_kw['scale'] = int(arg2)

    return col_type(**col_type_kw)



class DlcDialect(default.DefaultDialect):

    name = "dlc"

    driver = "dlc"

    engineGeneration = 'supersql'

    engineType = constants.EngineType.PRESTO

    max_identifier_length = 255

    cte_follows_insert = True

    supports_statement_cache = False

    encoding = 'UTF8'

    default_paramstyle = "pyformat"

    convert_unicode = True

    supports_unicode_statements = True
    
    supports_unicode_binds = True

    description_encoding = None

    postfetch_lastrowid = False

    supports_sane_rowcount = True

    implicit_returninga = False

    supports_sane_multi_rowcount = True

    supports_native_decimal = True

    supports_native_boolean = True

    supports_alter = True

    supports_multivalues_insert = True

    supports_comments = True

    supports_default_values = False

    supports_sequences = False



    preparer = DlcIdentifierPreparer
    ddl_compiler = DlcDDLCompiler
    type_compiler = DlcTypeCompiler
    statement_compiler = DlcCompiler
    execution_ctx_cls = DlcExecutionContext

    catalog = None

    schema = None

    def _get_default_schema_name(self, connection):
        return self.schema

    @classmethod
    def dbapi(cls):
        import tdlc_connector
        return  tdlc_connector
    
    @classmethod
    def import_dbapi(cls):
        import tdlc_connector
        return  tdlc_connector

    def create_connect_args(self, url):
        '''
        RFC1738: https://www.ietf.org/rfc/rfc1738.txt
        dialect+driver://username:password@host:port/database

        支持两种配置方式:

        1. dlc://ak:sk(:token)@region/database?engine=engineName&engine-type&arg1=value1
        2. dlc:///?secretId=1&secretKey=2&token

        {'host': 'ap-shanghai', 'database': 'public-engine:spark', 'username': 'ak', 'password': 'sk:token'}

        '''
        opts = url.translate_connect_args()
        query = dict(url.query)

        region = opts.get('host')
        secret_id = opts.get('username') 
        secret_key = opts.get('password')
        token = query.pop('token', None)
        self.engineGeneration = query.pop('engineGeneration', 'supersql')
        self.engineType = query.pop('engineType', constants.EngineType.PRESTO)

        if secret_key and secret_key.find(':') > 0:
            secrets = secret_key.split(':')
            secret_key = secrets[0]
            token = secrets[-1]

        self.schema = opts.get('database')

        self.catalog = opts.get('catalog', constants.Catalog.DATALAKECATALOG)

        kwargs = {
            'region': region or query.pop('region', None),
            'secret_id': secret_id or query.pop('secretId', None),
            'secret_key': secret_key or query.pop('secretKey', None),
            'token': token or query.pop('token', None),
            'endpoint': query.pop('endpoint', None),
            'engine': query.pop('engine', None),
            'resource_group':query.pop('resourceGroup', ''),
            'engine_type': self.engineType,
            'download': query.pop('download', False),
            'mode': query.pop('mode', constants.Mode.LASY)
        }

        return[[], kwargs]
    
    @reflection.cache
    def get_schema_names(self, connection, **kw):
        """
        Gets all schema names.
        """
        print(self.engineGeneration)
        print(self.engineType)
        cursor = connection.execute(
            text("SHOW /* tdlc:sqlalchemy:get_schema_names */ SCHEMAS")
        )

        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        """
        Gets all table names.
        """
        schema = schema or self.default_schema_name
        current_schema = schema
        ret = []
        if schema:
            cursor = connection.execute(
                text(
                    f"SHOW /* tdlc:sqlalchemy:get_table_names */ TABLES IN {schema}"
                )
            )

            if self.engineGeneration == "native" and self.engineType == constants.EngineType.SPARK:
                ret = [self.normalize_name(row[1]) for row in cursor]
            else:
                ret = [self.normalize_name(row[0]) for row in cursor]
            # ret = [self.normalize_name(row[0]) for row in cursor]
        return ret
    
    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        """
        Gets all view names
        """
        ret = []
        if self.engineGeneration == "native" and self.engineType == constants.EngineType.PRESTO:
            return ret
        schema = schema or self.default_schema_name
        if schema:
            cursor = connection.execute(
                text(
                    f"SHOW /* tdlc:sqlalchemy:get_view_names */ VIEWS IN {schema}"
                )
            )
            if self.engineGeneration == "native" and self.engineType == constants.EngineType.SPARK:
                ret = [self.normalize_name(row[1]) for row in cursor]
            else:
                ret = [self.normalize_name(row[0]) for row in cursor]
            # ret = [self.normalize_name(row[0]) for row in cursor]
        return ret
    
    def get_table_comment(self, connection, table_name, schema, **kw):

        schema = schema or self.default_schema_name

        ret = ""
        if self.engineGeneration == "native" and self.engineType == constants.EngineType.PRESTO:
            return {
                "text": None
            }

        if schema:
            cursor = connection.execute(
                text(f"SHOW /* tdlc:sqlalchemy:get_table_comment*/ TBLPROPERTIES {schema}.{table_name}")
            )
            ret = {row[0]: row[1] for row in cursor}
        return {
            "text": ret.get("comment", None)
        }

    @reflection.cache
    def get_columns(self, connection, table_name, schema, **kw):

        schema = schema or self.default_schema_name
        ret = []
        if self.engineGeneration == "native" and self.engineType == constants.EngineType.SPARK:
            if schema:
                cursor = connection.execute(
                    text(f"DESCRIBE /* tdlc:sqlalchemy:get_columns*/ {schema}.{table_name}")
                )

                for row in cursor:
                    if row[0] == "" or row[1] == "" or row[0].find("# Partitioning") == 0 or row[0].find("Part ") == 0 \
                            or row[0].find("Not partitioned") == 0:
                        continue
                    column = {
                        'name': row[0],
                        'type': get_column_type(row[1])
                    }
                    ret.append(column)
        else:
            if schema:
                cursor = connection.execute(
                    text(f"SHOW /* tdlc:sqlalchemy:get_columns*/ COLUMNS IN {schema}.{table_name}")
                )

                for row in cursor:
                    column = {
                        'name': row[0],
                        'type': get_column_type(row[1])
                    }
                    ret.append(column)

        return ret

    def get_indexes(self, connection, table_name, schema, **kw):
        ''' 不支持 '''
        return []
    
    def get_pk_constraint(self, connection, table_name, schema, **kw):
        ''' 不支持 '''
        return []
    
    def get_foreign_keys(self, connection, table_name, schema, **kw):
        ''' 不支持 '''
        return []
    
    def has_table(self, connection, table_name, schema, **kw) -> None:

        schema = schema or self.default_schema_name

        try:
            r = connection.execute(
                text(f"DESC /* tdlc:sqlalchemy:has_table */ {schema}.{table_name}")
            )
            row = r.fetchone()
            return row is not None
        except Exception as e:
            # TODO 异常分类
            return False
    
    def has_index(self, connection, table_name, index_name, schema, **kw):
        return False
    
    def has_sequence(self, connection, sequence_name, schema, **kw) -> None:
        return False



dialect = DlcDialect
