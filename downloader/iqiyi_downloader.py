# coding: utf-8
"""下载爱奇艺的相关信息"""

from downloader import *


log_path = os.path.join(log_dir, 'iqiyi.log')
logger = initial_log(log_path)


def iqiyi_show_downloader():
    """
    爱奇艺综艺模块下载
    :return: 
    """
    # 爱奇艺综艺模块的URL
    # sql = "SELECT URL FROM t0102_source WHERE STATUS = 0 AND PlatForm = '101' AND TYPE = '01'"
    # result = select(logger, sql, None)[0]
    # for item in result:
    url = 'http://www.iqiyi.com/zongyi/'
    showList = []
    res = requests.get(url, timeout=10)
    res.encoding = 'utf-8'
    text = res.text
    html_content = html.fromstring(text)
    # 第一模块
    selector1 = '#block-E > div.flow-twoBlock.clearfix > div.qy-col.col-2 > div > ul > li > div.site-piclist_pic > a'
    show_block1 = html_content.cssselect(selector1)
    platform = "101"  # 爱奇艺的编码
    updateDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    for ele in show_block1:
        name = ele.get('title')
        url = ele.get('href')
        image_url = ele.cssselect("img")[0].get('src')
        issue = ele.cssselect(".mod-listTitle_right")[0].text
        des = html_content.cssselect("#block-E > div.flow-twoBlock.clearfix > div.qy-col.col-2 > div > ul > li > "
                                     "div.site-piclist_info > p.site-piclist_info_describe.unPgc-info_describe")[0].text
        showList.append((name, issue, url, des, image_url, platform, updateDate))
        # print issue
    # 第二模块
    selector2 = '#block-E > div.flow-twoBlock.clearfix > div.o-hidden > div.wrapper-piclist > ul >li'
    show_block2 = html_content.cssselect(selector2)

    sql = "REPLACE INTO t0103_show (NAME, Issue, URl, Des, ImageURL, PlatForm, UpdateDate) " \
          "VALUE (%s, %s, %s, %s, %s, %s, %s)"

    batch_update(logger, sql, showList)


# ###########################################
def iqiyi_downloader():
    """
    爱奇艺官网下载入口
    :return: 
    """
    # 综艺模块
    iqiyi_show_downloader()


iqiyi_downloader()