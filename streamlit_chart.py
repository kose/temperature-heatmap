# streamlit でグラフを描画する
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns

##
## CSVファイルを読み込む(場所ごとの気温データ)
##
def read_temperature(place):

    resource_dir = 'csv'

    # resource_dir にあるファイルをリスト化
    files = os.listdir(resource_dir)

    # ファイル名のリストから weather_*.csv ファイルのみを抽出
    csv_files = [file for file in files if file.startswith(f"{place}") and file.endswith('.csv')]
    
    # ソートする
    csv_files.sort()

    # csv ファイルを読み込みこみ、ひとつのデータフレームに結合
    df = pd.concat([pd.read_csv(f'{resource_dir}/{file}') for file in csv_files], ignore_index=True)

    # nanを含む行を削除
    df = df.dropna()

    return df


##
## ヒートマップを描画
##
def show_heatmap(place, show_type):

    df = read_temperature(place)

    # 平均気温の列を取り出す
    temp= '平均気温'
    # temp= '最高気温'
    df = df[['年月日', temp]]

    # 最初の年を取得
    first_year = int(df['年月日'].str[:4].min())
    
    # 5度刻みで色分けされるようにする
    if show_type == '5度刻み':
        df[temp] = df[temp].apply(lambda x: 5 * round(x / 5, 0))

    # ヒートマップの描画
    plt.figure(figsize=(20, 10))

    # cmapの値は、https://matplotlib.org/stable/tutorials/colors/colormaps.html から選択
    colormap = 'jet'
    sns.heatmap(df.pivot_table(index=df['年月日'].str[:4], columns=df['年月日'].str[5:], values=temp, aggfunc='mean'), cmap=colormap)


    # y軸のラベルは、10年ごとに表示、first_year から 2024年まで
    plt.yticks(ticks=range(0, 2024 - first_year, 10), labels=[str(year) for year in range(first_year, 2024, 10)])
    plt.ylabel('年')

    # X軸のラベルは、月ごとに表示
    plt.xticks(ticks=[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])   
    plt.xlabel('月')

    return plt


##
## メインの処理 (streamlit)
##
def main():

    # ページ全体のレイアウトを設定
    st.set_page_config (layout="wide",)

    # タイトル
    st.title('1日の平均気温のヒートマップ')
    
    # 場所をラジオボタンで選択
    from scraping import url_dic
    place = st.radio('場所を選択してください', url_dic.keys(), index=2, horizontal=True)

    # 表示方法を選択
    show_type = st.radio('表示方法を選択してください', ['通常ヒートマップ', '5度刻み'], index=1, horizontal=True)

    # ヒートマップを描画
    plt = show_heatmap(place, show_type)

    # グラフを表示
    st.pyplot(plt, use_container_width=True)


if __name__ == '__main__':
    main()

# import pdb; pdb.set_trace()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
