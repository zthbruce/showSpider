# coding:utf-8
# __init__.py

# 引入模块
import sys
import os
import re
import traceback
import logging
import logging.handlers
import MySQLdb
import requests
from lxml import html
from DBUtils.PooledDB import PooledDB
import conf

# 日志先行
# 脚本当前目录
current_path = sys.path[0]

# 日志文件所在目录
log_dir = os.path.join(current_path, 'log')

# 数据库连接池
pool = PooledDB(MySQLdb, mincached=conf.pool_min_cached, maxcached=conf.pool_max_cached, maxconnections=conf.pool_size,
                blocking=True, host=conf.mysql_host, user=conf.mysql_user, passwd=conf.mysql_pwd, db=conf.mysql_db, port=conf.mysql_port)


# 更新数据库
def update(logger, sql, param):
    """
    :param logger: 日志记录
    :param sql: 待执行的sql语句
    :param param: sql语句的参数
    :return: 
    """
    try:
        con = pool.connection()
        cur = con.cursor()
        if param is not None:
            cur.execute(sql, param)
        else:
            cur.execute(sql)
        con.commit()

        cur.close()
        con.close()
    except Exception, e:
        logger.exception('sql error : %s', sql)


# 查询数据库
def select(logger, sql, param):
        try:
            con = pool.connection()
            cur = con.cursor()
            if param is None:
                cur.execute(sql)
            else:
                cur.execute(sql, param)
            result_list = cur.fetchall()
            cur.close()
            con.close()
            return result_list
        except Exception, e:
            logger.exception('sql error : %s', sql)
            return None


# 初始化日志
def initial_log(log_path):
    try:
        # 保证日志目录是否存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger("equasis")
        logger.setLevel(logging.DEBUG)
        trf_handler = logging.handlers.TimedRotatingFileHandler(log_path, 'H', 1, 0)
        trf_handler.suffix = "%Y%m%d-%H.log"
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d %(message)s ',
                                      '%a, %d %b %Y %H:%M:%S')
        trf_handler.setFormatter(formatter)
        logger.addHandler(trf_handler)
        return logger
    except Exception, e:
        logger.exception('can\'t create logger object!')
