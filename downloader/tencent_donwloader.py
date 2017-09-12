# coding: utf-8

from downloader import *

log_path = os.path.join(log_dir, 'tencent.log')
print log_path
logger = initial_log(log_path)
today = datetime.date.today()

# 下载网页内容
platform = "102"  # 爱奇艺的编码
source_url = 'https://v.qq.com/x/variety/'
res = requests.get(source_url, timeout=10)
res.encoding = 'utf-8'
text = res.text
html_content = html.fromstring(text)


# 热点模块下载
def hot_show_downloader():
    updateDate = str(today)
    showList = []
    hot_selector = "#new_vs_focus > div.slider_nav > a"
    hot_content = html_content.cssselect(hot_selector)
    for content in hot_content:
        url = content.get("href")
        # print url
        name = content.cssselect(".tit")[0].text
        des = content.cssselect(".txt")[0].text
        big_image = content.get("data-bgimage")
        small_image = ""
        showList.append((url, name, platform, des, big_image, small_image, updateDate))
    sql = "REPLACE INTO t0104_hot (URl, NAME, PlatForm, Des, BigImage, SmallImage, UpdateDate) " \
          "VALUE (%s, %s, %s, %s, %s, %s, %s)"
    batch_update(logger, sql, showList)


# 最近一周综艺节目单
def get_show_list_latest():
    showList = []
    day_selector = "#timetable > div.mod_bd > div.mod_schedule > div"
    week_content = html_content.cssselect(day_selector)
    i = 0
    for day_content in week_content:
        if i == 0:
            delta = 0
        else:
            delta = 7 - i
        updateDate = str(today - datetime.timedelta(delta))
        day_content_list = day_content.cssselect(".update_item")
        for content in day_content_list:
            title_content = content.cssselect("a")[0]
            url = title_content.get("href")
            name = title_content.get("title")
            issue = title_content.cssselect(".figure_count")[0].text.strip()
            print issue
            image_url = title_content.cssselect("img")[0].get("src")
            detail_content = content.cssselect(".figure_desc")[0]
            des = detail_content.get("title")
            showList.append((name, issue, url, des, image_url, platform, updateDate))
        i += 1
    print len(showList)
    sql = "REPLACE INTO t0105_update (NAME, Issue, URl, Des, ImageURL, PlatForm, UpdateDate) " \
          "VALUE (%s, %s, %s, %s, %s, %s, %s)"
    batch_update(logger, sql, showList)


def tencent_downloader():
    # 热门综艺
    hot_show_downloader()
    # 一周综艺
    get_show_list_latest()
tencent_downloader()

