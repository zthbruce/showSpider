# coding: utf-8
"""下载爱奇艺的相关信息"""

from downloader import *

log_path = os.path.join(log_dir, 'iqiyi.log')
logger = initial_log(log_path)
today = datetime.date.today()

# 下载爱奇艺综艺的网页
source_url = 'http://www.iqiyi.com/zongyi/'
res = requests.get(source_url, timeout=10)
res.encoding = 'utf-8'
text = res.text
html_content = html.fromstring(text)
platform = "101"


# 获取综艺的具体内容
def get_show_content(ul_element):
    updateDate = str(today)
    show_list = []
    # 遍历每个li进行设置
    print len(ul_element)
    for li in ul_element:
        ele = li.cssselect("div.site-piclist_pic > a")[0]
        name = ele.get('title')
        url = ele.get('href')
        image_url = ele.cssselect("img")[0].get('src')
        issue = ele.cssselect(".mod-listTitle_right")[0].text
        des = li.cssselect("div.site-piclist_info > p.site-piclist_info_describe.unPgc-info_describe")[0].text
        show_list.append((name, issue, url, des, image_url, platform, updateDate))
        # print(name, issue, url, des, image_url, platform, updateDate)
    return show_list


# 强档推荐
def iqiyi_show_downloader():
    # 强档推荐板块
    # 第一模块,最左边的大图
    showList = []
    selector1 = '#block-E > div.flow-twoBlock.clearfix > div.qy-col.col-2 > div > ul > li'
    show_block_1 = html_content.cssselect(selector1)
    show_block_1_content = get_show_content(show_block_1)
    showList.extend(show_block_1_content)
    # 第二模块, 右边上层列表
    selector2 = '#block-E > div.flow-twoBlock.clearfix > div.o-hidden > div.wrapper-piclist > ul >li'
    show_block_2 = html_content.cssselect(selector2)
    show_block_2_content = get_show_content(show_block_2)
    showList.extend(show_block_2_content)
    # 第三模块, 右边下层列表
    selector3 = '#block-E > div.flow-twoBlock.clearfix > div.o-hidden > div.clearfix > ' \
                'div.site-main-outer > div > div > ul > li'
    show_block_3 = html_content.cssselect(selector3)
    show_block_3_content = get_show_content(show_block_3)
    showList.extend(show_block_3_content)
    sql = "REPLACE INTO t0103_show (NAME, Issue, URl, Des, ImageURL, PlatForm, UpdateDate) " \
          "VALUE (%s, %s, %s, %s, %s, %s, %s)"
    batch_update(logger, sql, showList)


# 热点模块下载
def hot_show_downloader():
    showList = []
    updateDate = str(today)
    small_selector = "#j-focusBtn > li > a"
    big_selector = "#widget-midumfocuspicture > div.focusOne-wrapper.focusOne-wrapper-npt > div.focus_threeImg"
    hot_block = html_content.cssselect(small_selector)
    big_block = html_content.cssselect(big_selector)[0]
    i = 4
    for ele in hot_block:
        # 名称
        name = ele.get("title")
        # url
        url = ele.get('href')
        # 描述
        des = ele.get("data-mediumfocuspicture-description")
        # 小图
        small_image = ele.cssselect("img")[0].get('src')
        # 大图
        big_image = big_block.cssselect("div:nth-child(" + str(i) + ") > img")[0].get("src")
        showList.append((url, name, platform, des, big_image, small_image, updateDate))
        # print(url, name, platform, des, big_image, small_image, updateDate)
        i += 1
    sql = "REPLACE INTO t0104_hot (URl, NAME, PlatForm, Des, BigImage, SmallImage, UpdateDate) " \
          "VALUE (%s, %s, %s, %s, %s, %s, %s)"
    batch_update(logger, sql, showList)


# 最近一周综艺节目单
def get_show_list_latest():
    showList = []
    day_selector = "#widget-qycpweekly > div.weekline_item"
    week_content = html_content.cssselect(day_selector)
    # 遍历一周
    i = 0
    for day_content in week_content:
        if i == 0:
            delta = 0
        else:
            delta = 7 - i
        updateDate = str(today - datetime.timedelta(delta))
        day_content_list = day_content.cssselect("ul > li > div > a")
        # 遍历某一天的综艺
        for content in day_content_list:
            url = content.get("href")
            title_content = content.cssselect(".weekLink_title")[0]
            name = title_content.cssselect("h4")[0].text
            des = title_content.cssselect("p")[0].get("title")
            image_content = content.cssselect(".weekLink_img")[0]
            image_url = image_content.cssselect("img")[0].get("src")
            issue = image_content.cssselect(".mod-listTitle_right")[0].text
            # print(name, issue, url, des, image_url, platform, updateDate)
            showList.append((name, issue, url, des, image_url, platform, updateDate))
        i += 1
    sql = "REPLACE INTO t0105_update (NAME, Issue, URl, Des, ImageURL, PlatForm, UpdateDate) " \
          "VALUE (%s, %s, %s, %s, %s, %s, %s)"
    batch_update(logger, sql, showList)


# ###########################################
def iqiyi_downloader():
    # 综艺模块
    iqiyi_show_downloader()
    # 热点综艺下载
    hot_show_downloader()
    # 综艺节目单下载
    get_show_list_latest()

# 爱奇艺的综艺下载
iqiyi_downloader()
