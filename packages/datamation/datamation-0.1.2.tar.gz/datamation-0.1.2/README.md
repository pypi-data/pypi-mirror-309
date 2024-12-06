# Datamation
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic)


#### 特性

- 不同数据库中大批量数据的导入、导出，ETL数据同步
- 关系型数据库的数据导入到ElsticSearch
- 数据库表结构差异比对、整表数据差异比对，定位到行列级别
- 消息通知，支持邮件、钉钉、企业微信

## 安装

1. 拉取git项目到本地
2. pip install datamation

#### 基本使用

初始化连接
```python
import pymysql 
import datamation as dm

# 创建数据源连接
src_conn = lambda:pymysql.connect(host='127.0.0.1',user='root',passwd='xxx',database='demo',port=13307,write_timeout=50000,connect_timeout=20000)

# 创建目标数据库连接
tag_conn = lambda:pymysql.connect(host='127.0.0.1',user='root',passwd='xxx',database='demo',port=13306,read_timeout=50000,connect_timeout=10000)

```

示例1
```python
dm.sqlsync(
        src_conn = src_conn,
        src_table='table1',
        tag_conn = tag_conn,
        tag_table='table2',
        batch_size=20000, # 批量写入行数
        truncate=True   # 同步开始时使用truncate命令清空目标数据表
        ) 

```

示例2
```python

src = dm.source_sql(src_conn,'table1')
tag = dm.table_basic(tag_conn,'table1',columns =['col1','col2','col3'],batch_size=20000)
for row in src:
    tag.insert(row)
tag.endload()
```

##### 数据库差异检测

校验两个数据表数据值是否一致，返回差异数据
1 当主键为数值类型时，使用主键进行比对
```python
comp = dm.get_sqldata_diff2(src_conn,tag_conn,'tb_data','tb_data_copy1',compare_field='id')
print(comp)

```
2. 当主键为uuid类型时

```python
comp = dm.get_sqldata_diff1(src_conn,tag_conn,'tb_data','tb_data_copy1',compare_field='id',)
print(comp)

```
表结构差异比对 基于sqlalchemy
```python
comp = dm.get_sqldb_diff(src_conn,tag_conn,'tb_data','tb_data_copy1')
print(comp)

```

##### 消息通知
集成有邮件、钉钉、企业微信的消息推送

邮件消息发送
示例1 
```python
# 示例1
import datamation as dm
tm = dm.to_mail(user,passwd,host)
tm.name('hello word',to = ['xxx@xx.com','xxx@xxx.com'],
                            cc=  ['xxx@xx.com','xxx@xxx.com'],
                            bcc=  ['xxx@xx.com','xxx@xxx.com'],
            showname = 'datamation')
tm.add_text('hello word')
tm.add_html('<p> hello word</p> <img src=cid:image001.jpg style="height:71px; width:116px" />')
tm.add_related({'image001.jpg':'data/image001.jpg'}) # 添加在html中引用显示的图片内容
tm.add_attachment({'data.xlsx':'/data/data.xlsx'}) # 添加附件
tm.send()

```
示例2

```python
# 示例2
import datamation as dm
tm = dm.to_mail(user,passwd,host)
tm.send('hello word',
        to = ['xxx@xx.com'],
        cc=  [''],
        bcc= [''],
        showname = 'datamation',
        related = {'image001.jpg':'data/image001.jpg'},
        attachment = {'data.xlsx':'/data/data.xlsx'})
```

