# -*- coding: utf-8 -*-
__author__ = 'zhuqiuhan'

import urllib2
import gzip
from cStringIO import StringIO
import re
import csv
import socket

def GetPrice(url_detail,filename):
    final_url = url_detail.replace('xiangqing','chengjiao')

    p_2 = re.compile(r'''<span class="date">(.+?)</span>\s*<span class="TotalPrice org">(.+?)</span>\s*<span class="UnitPrice"  >(.+?)</span>\s*<span class="layout">(.+?)</span>\s*<span class="area">(.+?)</span>\s*<span class="louceng">(.+?)</span>\s*<span class="louceng">(.+?)</span>''')
    p_3 = re.compile(r'<a class="btnRight mt5 ml10 fl" href="(.+?)"></a>')

    csvfile_price = file(filename + '.csv','wb')
    writer_price = csv.writer(csvfile_price)
    writer_price.writerow(['成交日期','成交价','单价','户型','面积','楼层','朝向'])

    while True:
        try:
            list_req = urllib2.Request(final_url)
            list_response = urllib2.urlopen(list_req,timeout=500)
            list_page = list_response.read()
            html_list = list_page.decode('gbk','ignore').encode('utf-8')

        except socket.timeout,e:
            print 'Timeout when accessing 历史成交: '+final_url
        else:
            match_2 = p_2.findall(html_list)
            writer_price.writerows(match_2)

            match_3 = p_3.search(html_list)
            if match_3 is None:
                break
            else:
                final_url = match_3.group(1)

    csvfile_price.close()

csvfile = file('result.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['小区','地址','所属区域','邮编','竣工时间','当期户数','绿化率','容积率','停车位','交通','链接'])

p0 = re.compile(r'<div class="info rel floatl ml15">\s*<dl>\s*<.+>\s*<dt><a href="(http://.+?)"')
p1 = re.compile(r'<a id="xqw_B01_19" href="(.+?)" target')
#匹配下一页
p2 = re.compile(r'<a id="PageControl1_hlk_next" href="(.+?)">下一页</a>')

keyword_1 = re.compile(r'class="ewmBoxTitle">\s*<span class="floatl">(.+?)<')
keyword_2 = re.compile(r'''小区地址：</strong>(.+?)</dd>''')
keyword_3 = re.compile(r'''所属区域：</strong>(.+?)</dd>''')
keyword_4 = re.compile(r'''邮&nbsp;&nbsp;&nbsp;&nbsp;编：</strong>(.+?)</dd>''')
keyword_5 = re.compile(r'竣工时间：</strong>(.+?)</dd>')
keyword_6 = re.compile(r'<strong>当期户数：</strong>(.+?)</dd>')
keyword_7 = re.compile(r'绿 化 率：</strong>(.+?)</dd>')
keyword_8 = re.compile(r'<strong>容 积 率：</strong>(.+?)</dd>')
keyword_9 = re.compile(r'<strong>停 车 位：</strong>(.+?)</dt>')
keyword_10 = re.compile(r'<!--交通状况 begin-->.+?<dt>(.+?)</dt>',re.DOTALL)

#主要需要修改的部分在此处
#89为行政区网页号，13为页数
#通过查看fang.com上的网址来确定行政区网页号，修改此处即可
current_url = 'http://esf.sz.fang.com/housing/13080__1_0_0_0_1_0_0/'

while True:
    req = urllib2.Request(current_url)
    response = urllib2.urlopen(req)
    page = response.read()
    page_n = gzip.GzipFile(fileobj=StringIO(page), mode='r')
    html = page_n.read().decode('gbk').encode('utf-8')

    match = p0.findall(html)

    for matchurl in match:

        #add here for further link to 小区详情
        try:
            req_link = urllib2.Request(matchurl)
            response_link = urllib2.urlopen(req_link,timeout=300)
            page_link = response_link.read()
            page_link_unzip = gzip.GzipFile(fileobj=StringIO(page_link),mode='r')
            html_link = page_link_unzip.read().decode('gbk','ignore').encode('utf-8')
            match_1 = p1.search(html_link)
        except socket.timeout,e:
            print 'Error: ' + matchurl
        except urllib2.HTTPError,e:
            print e.code
        except urllib2.URLError,e:
            print e.reason

        else:
            try:
                com_req = urllib2.Request(match_1.group(1))
                com_response = urllib2.urlopen(com_req,timeout=300)
                com_page = com_response.read()
                com_page_unzip = gzip.GzipFile(fileobj=StringIO(com_page), mode='r')
                com_html = com_page_unzip.read().decode('gbk','ignore').encode('utf-8')
            except socket.timeout,e:
                print 'Timeout when accessing 小区详情: ' + match_1.group(1)

            else:
                p = []
                p.append(keyword_1)
                p.append(keyword_2)
                p.append(keyword_3)
                p.append(keyword_4)
                p.append(keyword_5)
                p.append(keyword_6)
                p.append(keyword_7)
                p.append(keyword_8)
                p.append(keyword_9)
                p.append(keyword_10)

                input_line = []
                for pat in p:
                    com_match = pat.search(com_html)
                    if com_match is None:
                        input_line.append('n/a')
                    else:
                        input_line.append(com_match.group(1))

                input_line.append(match_1.group(1))
                print input_line[0]

                writer.writerow(input_line)
                GetPrice(match_1.group(1),input_line[0])

    match_nextpage = p2.search(html)
    if match_nextpage is None:
        break
    else:
        print match_nextpage.group(1)
        current_url = 'http://esf.sz.fang.com' + match_nextpage.group(1)

csvfile.close()