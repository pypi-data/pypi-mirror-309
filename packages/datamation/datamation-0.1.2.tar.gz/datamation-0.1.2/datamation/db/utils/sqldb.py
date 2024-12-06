from collections import defaultdict
from .general import get_dialect_name,get_sqlalchemy_engine

def compare_tables(source_db, target_db,charset=False,collation=False):
    '''定义比对方法，用于比对两个数据库中的表结构差异
    '''
    from sqlalchemy import MetaData,event,String
    from sqlalchemy.ext.compiler import compiles
    from sqlalchemy.schema import CreateTable,DropTable

    # 创建两个 MetaData 对象，分别对应原始数据库和目标数据库
    source_meta = MetaData()
    target_meta = MetaData()

    @event.listens_for(source_meta, "column_reflect")
    def genericize_datatypes(inspector, tablename, column_dict):
        column_dict["type"] = column_dict["type"].as_generic()
        if not charset:
            column_dict["type"].charset=''
        if not collation:
            column_dict["type"].collation=''

    @event.listens_for(target_meta, "column_reflect")
    def genericize_datatypes(inspector, tablename, column_dict):
        column_dict["type"] = column_dict["type"].as_generic()
        if not charset:
            column_dict["type"].charset=''
        if not collation:
            column_dict["type"].collation=''

    @compiles(String, "mysql")
    def compile_text_mysql(type_, compiler, **kw):
        if kw and kw['type_expression'].type.length is None:
            return 'text'
        return str(type_)
    
    @compiles(String, "oracle")
    def compile_text_oracle(type_, compiler, **kw):
        if kw and kw['type_expression'].type.length is None:
            return 'varchar2(4000)'
        return str(type_)

    # 读取原始数据库的表结构
    source_meta.reflect(bind=source_db)
    # 读取目标数据库的表结构
    target_meta.reflect(bind=target_db)

    source = source_meta.tables
    target = target_meta.tables

    # 存储表结构差异的列表
    diff = []

    # 遍历原始数据库中的表
    for table_name, table in target.items():
        # 如果目标数据库中不存在该表，则将该表加入差异列表
        if table_name not in source:
            diff.append({
                'operation': 'remove_table',
                'table_name': table_name
            })

    # 遍历原始数据库中的表
    for table_name, table in source.items():
        # 如果目标数据库中不存在该表，则将该表加入差异列表
        if table_name not in target:
            
            diff.append({
                'operation': 'add_table',
                'table_name': table_name.upper(),
                'table':table,
                'ddl':str(CreateTable(table).compile(target_db)),
                'columns': [{'name': column.name.upper(), 
                             'type': column.type,
                             'default':column.server_default.arg.text if column.server_default else '',
                             'comment' :column.comment if column.comment else '',
                             'nullable':column.nullable,
                             'primary_key':column.primary_key
                             } 
                            for column in table.columns]
            })
        else:
            # 如果原始数据库和目标数据库都存在该表，则比对列的差异
            source_columns = {column.name.upper(): column for column in source[table_name].columns}
            target_columns = {column.name.upper(): column for column in target[table_name].columns}
            # 遍历原始数据库中的列
            for column_name, column in source_columns.items():
                # 如果目标数据库中不存在该列，则将该列加入差异列表
                if column_name not in target_columns:
                    diff.append({
                        'operation': 'add_column',
                        'table_name': table_name.upper(),
                        'column_name': column_name,
                        'type': column.type,
                        'default':column.server_default.arg.text if column.server_default else '',
                        'comment' :column.comment if column.comment else '',
                        'nullable':column.nullable
                    })
                else:
                    # 如果原始数据库和目标数据库都存在该列，则比对列的类型
                    source_type = source_columns[column_name].type
                    target_type = target_columns[column_name].type

                    # 如果类型不同，则将该列加入差异列表
                    if str(source_type) != str(target_type):
                        diff.append({
                            'operation': 'alter_column',
                            'table_name': table_name.upper(),
                            'column_name': column_name.upper(),
                            'type': source_type,
                            'default':column.server_default.arg.text if column.server_default else '',
                            'comment' :column.comment if column.comment else '',
                            'nullable':column.nullable,
                            'current_type': target_type
                        })

            # # 遍历目标数据库中的列
            for column_name, column in target_columns.items():
                # 如果原始数据库中不存在该列，则将该列加入差异列表
                if column_name not in source_columns :
                    diff.append({
                        'operation': 'remove_column',
                        'table_name': table_name.upper(),
                        'column_name': column_name.upper()
                    })

            # 比对索引差异
            source_indexes = {index.name: index for index in source[table_name].indexes}
            target_indexes = {index.name: index for index in target[table_name].indexes}
            # 遍历原始数据库中的索引
            for index_name, index in source_indexes.items():
                # 如果目标数据库中不存在该索引，则将该索引加入差异列表
                if index_name not in target_indexes:
                    diff.append({
                        'operation': 'add_index',
                        'table_name': table_name.upper(),
                        'index_name': index_name.upper(),
                        'type': getattr(index, 'type', ''),
                        'columns': [column.name for column in index.columns]
                    })

            # # 遍历原始数据库中的索引
            # for index_name, index in source_indexes.items():
            #     if index_name not in target_indexes:
            #         diff.append({
            #         'operation': 'remove_index',
            #         'table_name': table_name,
            #         'index_name': index_name
            #         })

    # 返回表结构差异列表
    return diff

def get_sqldb_diff(source_conn, target_conn,charset=False,collation=False):
    '''生成数据库结构差异脚本 需要sqlschema模块支持

    Parameters
    ----------
    source_db : dbapi2.Connection,function object returning a dbapi2.Connection
        原始数据库连接对象，或者是一个函数对象，该函数返回一个 dbapi2.Connection 对象
    target_db : dbapi2.Connection,function object returning a dbapi2.Connection
        目标数据库连接对象
    Returns
    -------
    list
        数据库结构差异脚本列表
    '''
    from sqlalchemy import create_engine, MetaData
    
    # 创建数据库引擎
    source_engine = get_sqlalchemy_engine(source_conn) #create_engine(f'{source_dialect_name}://',creator=source_db)
    target_engine = get_sqlalchemy_engine(target_conn) #create_engine(f'{target_dialect_name}://',creator=target_db)

    # 获取数据库元数据
    diff = compare_tables(source_engine, target_engine,charset=charset,collation=collation)

    # 创建空列表，用于存储 SQL 语句
    sql_statements = defaultdict(list)
    sql = ''
    # 遍历表结构差异
    for operation in diff:
        # 如果是创建表的操作，则生成创建表的 SQL 语句
        if operation['operation'] == 'add_table':
            sql = f"CREATE TABLE {operation['table_name']} ("
            for column in operation['columns']:
                column_type = column['type']
                # 处理字符集
                if not charset:
                    column_type.charset = ''
                if not collation:
                    column_type.collation = ''

                sql += f"{column['name']} {column['type'].compile(target_engine.dialect)} "
                if not column['nullable']:
                    sql+=' NOT NULL '
                if column['default']:
                    sql+=' default ' + column['default']
                if column['primary_key']:
                    sql+=' primary key'
                if column['comment']:
                    sql+=' comment ' + "'"+column['comment']+"'"
                
                sql += ","
            sql += ");"
            operation['sql'] = operation['ddl']
            sql_statements[operation['operation']].append(operation)

        # 如果是删除表的操作，则生成删除表的 SQL 语句
        if operation['operation'] == 'remove_table':
            sql = f"DROP TABLE {operation['table_name']};"
            operation['sql'] = sql
            sql_statements[operation['operation']].append(operation)

        # 如果是添加字段的操作，则生成添加字段的 SQL 语句
        if operation['operation'] == 'add_column':
            column_type = operation['type']

            # 处理字符集
            if not charset:
                column_type.charset=''
            if not collation:
                column_type.collation=''

            sql = f"ALTER TABLE {operation['table_name']} ADD COLUMN {operation['column_name']} {column_type.compile(target_engine.dialect)};"
            # if not column['nullable']:
            #     sql+=' NOT NULL'
            if operation['default']:
                sql+=' default ' + operation['default']
            if operation['comment']:
                sql+=' comment ' + operation['comment']
            operation['sql'] = sql+';'
            sql_statements[operation['operation']].append(operation)

        # 修改字段类型
        if operation['operation'] == 'alter_column': 
            column_type = operation['type']
            
            # 处理字符集
            if not charset:
                column_type.charset=''
            if not collation:
                column_type.collation=''

            sql = f"ALTER TABLE {operation['table_name']} MODIFY COLUMN {operation['column_name']} {column_type.compile(target_engine.dialect)} "
            if not operation['nullable']:
                sql+=' NOT NULL'
            if operation['default']:
                sql+=' default ' + operation['default']
            if operation['comment']:
                sql+=' comment ' + operation['comment']
            operation['sql'] = sql+';'
            operation['current_type'] = operation['current_type'].compile(target_engine.dialect)
            sql_statements[operation['operation']].append(operation)

        # 如果是删除字段的操作，则生成删除字段的 SQL 语句
        if operation['operation'] == 'remove_column':
            sql = f"ALTER TABLE {operation['table_name']} DROP COLUMN {operation['column_name']};"
            operation['sql'] = sql
            sql_statements[operation['operation']].append(operation)

        if operation['operation'] == 'add_index':
            # 生成新增索引的ddl语句
            if operation['type'] == 'primary_key':
                sql = f"ALTER TABLE {operation['table_name']} ADD PRIMARY KEY {operation['index_name']} ({','.join(operation['columns'])});;"
            elif operation['type'] == 'unique':
                sql = f"ALTER TABLE {operation['table_name']} ADD UNIQUE {operation['index_name']} ({','.join(operation['columns'])});;"
            else:
                sql = f"ALTER TABLE {operation['table_name']} ADD INDEX {operation['index_name']} ({','.join(operation['columns'])});"
            operation['sql'] = sql
            sql_statements[operation['operation']].append(operation)

        if operation['operation'] == 'remove_index':
            # 生成删除索引的ddl语句
            sql = f"ALTER TABLE {operation['table_name']} DROP INDEX {operation['index_name']};"
            operation['sql'] = sql
            sql_statements[operation['operation']].append(operation)

    # 返回 SQL 语句列表
    return sql_statements

def get_sqldb_ddl(conn,schema=None,charset='',collation='',exclude_charset=True,exclude_collation=True,to_conn=None,if_existing = True,keyword_case='upper'):
    ''' 基于sqlalchemy 获取数据库ddl

    Parameters
    ----------
    conn : dbapi2
        dbapi2数据库连接对象或函数 需要sqlalchemy支持
    schema : str, optional
        数据库名称, by default None
    charset : str, optional
        字符集, by default ''
    collation : str, optional
        校对集, by default ''
    exclude_charset : bool, optional
        是否排除字符集, by default True
    exclude_collation : bool, optional
        是否排除校对集, by default True
    to_conn : sqlalchemy.engine.base.Engine or sqlalchemy.engine.base.Connection or function, optional
        目标数据库连接对象或函数, by default None
    if_existing : bool, optional
        是否仅生成已存在的表, by default True
    keyword_case : str, optional
        关键字大小写, by default 'upper'
    '''
    from sqlalchemy import MetaData,create_engine
    from sqlalchemy.schema import CreateTable,DropTable

    from sqlalchemy import String
    from sqlalchemy.ext.compiler import compiles
    
    @compiles(String, "mysql")
    def compile_text_mysql(type_, compiler, **kw):
        if kw and kw['type_expression'].type.length is None:
            return 'text'
        return str(type_)
    
    @compiles(String, "oracle")
    def compile_text_oracle(type_, compiler, **kw):
        if kw and kw['type_expression'].type.length is None:
            return 'varchar2(4000)'
        return str(type_)
    
    source_engine = get_sqlalchemy_engine(conn) 
    
    if to_conn:
        target_engine = get_sqlalchemy_engine(to_conn)

    metadata = MetaData()
    metadata.reflect(bind=source_engine,schema=schema)

    create_table_ddl = []
    for table_name in metadata.tables:
        table = metadata.tables[table_name]
        if keyword_case == 'upper':
            table.name = table.name.upper()
        elif keyword_case == 'lower':
            table.name = table.name.lower()
        for column in table.columns:
            column.type = column.type.as_generic()
            column.name = column.name
            if keyword_case == 'upper':
                column.name = column.name.upper()
            elif keyword_case == 'lower':
                column.name = column.name.lower()
            
            if exclude_charset:
                column.type.charset=''
            if exclude_collation:
                column.type.collation=''
            if charset:
                if column.type.charset:
                    column.type.charset = charset
            if collation:
                if column.type.collation:
                    column.type.collation=collation
            table.append_column(column,replace_existing=True)
        
        if to_conn:
            if if_existing:
                sql =str(DropTable(table,if_exists =True).compile(target_engine))
                create_table_ddl.append(sql)
            sql = str(CreateTable(table).compile(target_engine))
            create_table_ddl.append(sql)
        else:
            if if_existing:
                sql =str(DropTable(table,if_exists =True))
                create_table_ddl.append(sql)
            sql = str(CreateTable(table))
            create_table_ddl.append(sql)
        
    return ';\n'.join(create_table_ddl)
