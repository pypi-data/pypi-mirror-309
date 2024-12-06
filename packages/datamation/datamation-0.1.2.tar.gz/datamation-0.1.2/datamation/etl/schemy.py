# 修改为sqlalchemy模式的表定义 
from sqlalchemy import Table,Column, Integer, String, DateTime, ForeignKey, JSON, Text, Boolean, BigInteger, Float, Date, Time, LargeBinary, SmallInteger, UniqueConstraint 
from sqlalchemy.ext.declarative import declarative_base

from ..db import get_dialect_name

Base = declarative_base()

class etl_dictionary(Base):
    __tablename__ = 'etl_dictionary'
    __table_args__ = (
        UniqueConstraint('category', 'item', name='unique_category_item'),
        {'comment': '字典表'}
    )
    id = Column(Integer, primary_key=True,comment='主键')
    category = Column(String(100), nullable=False,comment='类别')
    item = Column(String(100), nullable=False,comment='项目')
    value = Column(String(100), nullable=False,comment='值')
    comments = Column(String(100), nullable=False,comment='说明')
    create_date = Column(DateTime, nullable=False,comment='创建时间')

class etl_sources(Base):
    __tablename__ = 'etl_sources'
    __table_args__ = (
        UniqueConstraint('source_name', name='unique_source_name'),
        {'comment': '数据源表'}
    )
    id = Column(Integer, primary_key=True,comment='主键')
    source_name = Column(String(100), nullable=False,comment='数据源名称')
    category = Column(String(100), nullable=False,comment='数据源类型')
    connect_args = Column(JSON, nullable=False,comment='连接参数')
    comments = Column(String(100), nullable=False,comment='说明')
    create_date = Column(DateTime, nullable=False,comment='创建时间')

class etl_task_info(Base):
    __tablename__ = 'etl_task_info'
    __table_args__ = (
        UniqueConstraint('task_group', 'source_table', 'target_table', name='unique_task_group'),
        {'comment': '任务表'}
    )
    id = Column(Integer, primary_key=True,comment='主键')
    task_group = Column(String(100), nullable=False,comment='任务组')
    comments = Column(String(100), nullable=False,comment='表说明或者任务说明')
    source = Column(Integer, ForeignKey('etl_sources.id'), nullable=False,comment='源数据源id')
    source_table = Column(String(30), nullable=False,comment='源表')
    target = Column(Integer, ForeignKey('etl_sources.id'), nullable=False,comment='目标数据源id')
    target_table = Column(String(30), nullable=False,comment='目标表')
    is_increment = Column(Integer, nullable=False,comment='1 增量 0 全量')
    delete_factor = Column(String(1000), nullable=True,comment='删除条件')
    query_factor = Column(String(1000), nullable=True,comment='查询条件')
    delete_cusfactor = Column(String(1000), nullable=True,comment='自定义删除条件')
    status = Column(Integer, nullable=False,comment='状态 （1 启用 0 停用）')
    run_status = Column(Integer, nullable=False,comment='运行状态')
    before_sql = Column(String(2000), nullable=True,comment='同步前执行sql')
    affter_sql = Column(String(2000), nullable=True,comment='同步后执行sql')
    pks = Column(String(100), nullable=False,comment='主键')
    fieldsmap = Column(JSON, nullable=False,comment='字段映射')
    script = Column(JSON, nullable=False,comment='脚本')
    create_date = Column(DateTime, nullable=False,comment='创建时间')

class etl_task_log(Base):
    __tablename__ = 'etl_task_log'
    __table_args__ = (
        {'comment': '任务日志表'}
    )
    id = Column(Integer, primary_key=True,comment='主键')
    task = Column(Integer, ForeignKey('etl_task_info.id'), nullable=False,comment='任务id')
    log_text = Column(Text, nullable=False,comment='执行日志')
    log_file = Column(String(200), nullable=True,comment='日志文件')
    status = Column(Integer, nullable=False,comment='状态 （1 成功 0 失败）')
    start_time = Column(DateTime, nullable=False,comment='任务开始时间')
    end_time = Column(DateTime, nullable=False,comment='任务结束时间')
    create_date = Column(DateTime, nullable=False,comment='创建时间')

class etl_task_files(Base):
    __tablename__ = 'etl_task_files'
    __table_args__ = (
        {'comment': '任务文件表'}
    )
    id = Column(Integer, primary_key=True,comment='主键')
    task = Column(Integer, ForeignKey('etl_task_info.id'), nullable=False,comment='任务id')
    pathname = Column(String(200), nullable=False,comment='文件路径')
    filename = Column(String(200), nullable=False,comment='文件名')
    size = Column(Integer, nullable=False,comment='文件大小')
    create_date = Column(DateTime, nullable=False,comment='创建时间')

def init_etl_tables(conn):
    '''在数据库中创建etl配置表'''
    from sqlalchemy import create_engine
    if hasattr(conn,'__call__'):
        conn_db = conn()
        dialect = get_dialect_name(conn)
    else:
        conn_db = conn
        dialect = get_dialect_name(conn)

    
    engine = create_engine(f'{dialect}://',creator=conn_db)
    Base.metadata.create_all(engine)
    # 当表不存在时创建表
    etl_dictionary.create(engine, checkfirst=True)
    etl_sources.create(engine, checkfirst=True)
    etl_task_info.create(engine, checkfirst=True)
    etl_task_log.create(engine, checkfirst=True)
    etl_task_files.create(engine, checkfirst=True)
    
    # 向表中插入模拟数据
    etl_dictionary.insert().values(id=1,category='datasource',item='mysql',value=1,comments='启用').execute(engine)
    etl_dictionary.insert().values(id=2,category='datasource',item='oracle',value=1,comments='启用').execute(engine)
    etl_dictionary.insert().values(id=3,category='datasource',item='oss-aliyun',value=1,comments='启用').execute(engine)
    etl_dictionary.insert().values(id=4,category='datasource',item='xlsx',value=1,comments='启用').execute(engine)
    etl_dictionary.insert().values(id=5,category='datasource',item='csv',value=1,comments='启用').execute(engine)

    etl_sources.insert().values(id=1,category='mysql',connect_args = {'host':'','port':'','dbname':'','user':'','password':''},comments='mysql数据源').execute(engine)


    