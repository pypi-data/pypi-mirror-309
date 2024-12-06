
import gzip
import sys
import csv
import datetime as dt
import time
import locale
import subprocess
from pathlib import Path
from .source import source_sql 

__all__ = ['dbuldr','dump_sql','sqluldr2','dump_csv']

def dbuldr(conn,sql:str='',table_name:str='',save_file = '',output:str='csv',
           db_type = 'postgres',
           date_format = '%Y-%m-%d %H:%M:%S',
           escape_str = True,
           batch_size = 50000,
           insert_batch_size = 1,
           fieldsep=',',
           rowsep='\n\r',
           encoding = 'utf-8',
           included_head = True,
           archive = True):
    
    if output=='csv':
        return dump_csv(conn,sql,file = save_file,batch_size=batch_size,fieldsep=fieldsep,rowsep=rowsep,encoding=encoding,included_head=included_head,archive=archive)
    if output=='sql':
        return dump_sql(conn, table_name,save_file=save_file,db_type=db_type,date_format=date_format,escape_str=escape_str,batch_size=insert_batch_size)

def dump_csv(conn,sql='',save_file = None,batch_size = 50000,fieldsep=',',rowsep='\n\r',encoding='utf-8',included_head=True,archive =True):
    '''数据导出
    不同的数据库可能需要一些单独的方法在连接或者游标层处理一些特殊的数据类型 
    例oracle的cx_Oracle clob对象返回的并不是直接字符串 需要使用相应方法进行提取
    def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
            if defaultType == oracle.CLOB:
                return cursor.var(oracle.LONG_STRING, arraysize = cursor.arraysize)
    conn.outputtypehandler = OutputTypeHandler

    Parameters
    ------------
    conn:PEP249 API
    sql: str
        sql
    file:str
        文件名称
    batch_size:int
        批量加载行数
    delimiter:str
        字段分隔符 默认 ','
    encoding:str
        文件编码 默认utf-8
    db:str
        oracle、
        数据库类型
    archive:bool
        是否压缩文件 默认为True
    '''
    src = source_sql(conn,sql,data_format='list')
    data = []
    row_num = 0
    
    save_file = save_file if save_file else sql[:50]
    save_file = dt.datetime.now().strftime('%Y%m%d') + '_' + save_file

    if save_file.split('.')[-1] in ['GZ','gz'] or archive:
        file_obj = gzip.open
    else:
        file_obj = open

    head = src.cols
    with file_obj(save_file, 'wt', newline=rowsep,encoding=encoding) as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=fieldsep,lineterminator = '\r\n' ,quoting=csv.QUOTE_NONNUMERIC)
        if included_head:
            spamwriter.writerow(head)
        for n in src:
            data.append(n)
            if len(data) % batch_size == 0:
                row_num+=batch_size
                print(time.ctime(),'out row {}'.format(row_num))
                spamwriter.writerows(data)
                csvfile.flush()
                data = []
        if data:
            row_num+=len(data)
            spamwriter.writerows(data)
            print(time.ctime(),'out row {}'.format(row_num))
            data = []
    return True

def dump_sql(conn, table_name, 
    db_type='postgres', date_format='%Y-%m-%d %H:%M:%S', 
    insert_batch_size=1, escape_str=True,
    save_file =''
):
    """
    通用的 SQL INSERT 语句生成器，支持 PostgreSQL、MySQL、Oracle。
    
    :param sql: SQL 执行函数
    :param conn: 数据库连接对象
    :param table_name: 表名
    :param db_type: 数据库类型 ('postgres', 'mysql', 'oracle')
    :param date_format: 日期格式化字符串
    :param insert_batch_size: 每批次的插入行数，默认为 1
    :param escape_str: 是否启用字符串转义，默认启用
    :parm save_file: 保存为文件 
    :return: INSERT 语句列表
    """
    if not conn or not table_name:
        raise ValueError("数据库连接对象和表名不能为空")

    # 读取表数据并获取列名
    src = source_sql(conn, f'SELECT * FROM {table_name}', data_format='list')
    if not src:
        return []  # 如果没有数据，直接返回空列表

    cols = src.cols
    insert_sqls = []

    # 不同数据库的字符串转义前缀
    escape_prefix = {
        'postgres': "E'",   # PostgreSQL 支持 E'' 格式
        'mysql': "'",        # MySQL 使用普通单引号
        'oracle': "'"        # Oracle 同样使用普通单引号
    }

    # 基础 INSERT 语句模板
    base_sql = f'INSERT INTO {table_name} ({",".join(cols)}) VALUES '

    # 处理每一行数据，并按照批次生成 SQL
    batch = []
    for idx, row in enumerate(src):
        row_values = []
        for value in row.values():
            if isinstance(value, dt.datetime):  # 日期时间处理
                formatted_date = value.strftime(date_format)
                row_values.append(f"'{formatted_date}'")
            elif value is None:  # 处理 NULL 值
                row_values.append('NULL')
            elif isinstance(value, (float, int)):  # 数字类型直接转换
                row_values.append(str(value))
            elif isinstance(value, str):  # 字符串处理并转义
                escaped_value = value.replace("'", "''") if escape_str else value
                row_values.append(f"{escape_prefix[db_type]}{escaped_value}'")
            else:  # 其他类型转换为字符串
                row_values.append(f"'{str(value)}'")

        batch.append(f"({','.join(row_values)})")

        # 当达到批次大小或最后一行时，生成 INSERT 语句
        if (idx + 1) % insert_batch_size == 0 or idx + 1 == len(src):
            insert_sqls.append(base_sql + ',\n'.join(batch) + ';')
            batch = []

    file = Path(save_file)/table_name+'.sql'
    file.write_text('\n'.join(insert_sqls))
    return str(file.absolute())


def sqluldr2(user=None,query=None,sql=None,field = None,record = None,rows = None,file = None,log = None,
             fast = None,text = None,charset = None,ncharset = None,parfile = None,read = None,sort = None,hash = None,array = None,head =None,batch = None,size = None,
             serial = None,trace = None,table = None,control = None,mode = None,buffer = None,long = None,width = None,quote = None,data = None,alter = None,safe = None,
             crypt=None,sedf = None,null = None,escape = None,escf = None,format = None,exec = None,prehead = None,rowpre = None,rowsuf = None,colsep = None,presql =None,
             postsql = None,lob = None,lobdir = None,split = None,degree = None,hint = None,unique = None,update = None,parallel=None,skip = None,skipby = None,skipby2 = None,):
    '''sqluldr2 python封装
    sqluldr2是oracle的sqlldr的python封装 用于导出数据 与sqlldr的参数基本一致 但是有一些参数不支持 例如direct 、parallel

    Examples
    ---------
    sqluldr2(user='test',query='select * from test',file='test.csv',field='id,name',record='|',rows='|',head='Y',batch='Y',size=10000,mode='insert',buffer=100000,lob='Y',lobdir='lob',split='Y',degree=4,unique='id',update='name')
    '''
    kwargs = locals()
    args = []
    for k,v in kwargs.items():
        if v:
            args.append('{}={}'.format(k,v))
    if args:
        command = 'sqluldr2 ' +' '.join(args)
        return subprocess.run(command,capture_output=True,text = True)
    
