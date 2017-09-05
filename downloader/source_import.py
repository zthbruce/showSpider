# coding:utf-8

from downloader import *

# 日志文件
log_path = os.path.join(log_dir, 'import.log')
logger = initial_log(log_path)


def import_data_file():
    current_dir = sys.path[0]  # 当前模块的路径
    source_file = os.path.join(current_dir, 'source', 'source.csv')
    sql = "REPLACE INTO t0102_source (URL, PlatForm, TYPE, Des) VALUE (%s, %s, %s, %s)"
    with open(source_file, "r") as source:
        for line in source:
            line = line.strip()
            line_info = line.split(",")
            print line_info[3]
            update(logger, sql, (line_info[0], line_info[1], line_info[2], line_info[3]))


