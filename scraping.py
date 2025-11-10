#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import csv
import numpy as np
import urllib.request
from bs4 import BeautifulSoup

## 気象庁 気象観測データからデータ入手
## https://www.jma.go.jp/jma/menu/menureport.html
##
url_dic = {"札幌": [44, 47662],
           "山形": [35, 47588], 
           "東京": [44, 47662],
           "横浜": [46, 47670],
           "大阪": [62, 47772],
           "福岡": [82, 47807],
           }
##
## HTML table の値がなければ nan
##
def str2float(weather_data):
    try:
        return float(weather_data)
    except:
        return np.nan

##
## スクレイピング
##
def scraping(url, date):
    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    # print(url)
    soup = BeautifulSoup(html)
    trs = soup.find("table", { "class" : "data2_s" })

    data_per_month = []

    # table の中身を取得
    if trs is not None:
        for tr in trs.findAll('tr')[4:]:
            tds = tr.findAll('td')
 
            data_list = []
            data_list.append(date)
            data_list.append(str2float(tds[6].string))
            data_list.append(str2float(tds[7].string))
            data_list.append(str2float(tds[8].string))

            data_per_month.append(data_list)

            # dateを1日進める
            date += datetime.timedelta(days=1)

    return data_per_month


##
## CSVに保存
##
def create_csv(place, year):

    # csvディレクトリがなければ作成
    if not os.path.exists('csv'):
        os.makedirs('csv')

    # 出力ファイル名
    csv_file = f"csv/{place}_{year}.csv"

    # ファイルが存在する場合は終了
    if os.path.exists(csv_file):
        # print(f"{csv_file} is already exists.")
        return

    fields = ['年月日', '平均気温', '最高気温', '最低気温']

    with open(csv_file, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)

        # year の 1月〜12月の月のループ
        for month in range(1, 13):

            date = datetime.date(year, month, 1)

            prec_no = url_dic[place][0]
            block_no = url_dic[place][1]
            # print(f"place: {place}, prec: {prec_no}, block: {block_no}")

            # 対象url
            url = f"http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no={prec_no}&block_no={block_no}&year={date.year}&month={date.month}&day={date.day}&view="
            data_per_month = scraping(url, date)

            for data in data_per_month:
                writer.writerow(data)

    print(f"created {csv_file}")


if __name__ == '__main__':

    for place in url_dic.keys():
        for year in range(2025, 1871, -1):
            create_csv(place, year)

# import pdb; pdb.set_trace()

### Local Variables: ###
### truncate-lines:t ###
### End: ###


