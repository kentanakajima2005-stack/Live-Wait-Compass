import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Live-Wait Compass",layout="wide")

st.title("Live-Wait Compass")
st.markdown("～物販完了データを起点とした地域回遊・混雑分散ダッシュボード～")

try:
    #外部のCSVファイルを読み込む
    cafe_data = pd.read_csv('cafe_data.csv')
except FileNotFoundError:
    st.error("cafe_data.csvが見つかりません。")
    st.stop()

st.sidebar.header("リアルタイム分析")
current_time = st.sidebar.slider("現在時刻",10,18,13)
fans_simulation = {
    10: 3000,
    11: 5000,
    12: 8000,
    13: 15000,
    14: 25000,
    15: 35000,
    16: 38000,
    17: 20000,
    18: 5000
}

waiting_fans = fans_simulation.get(current_time, 0)

if current_time == 10:
    delta_text = "物販開始で増加中"
elif current_time >= 17:
    delta_text = "入場開始で減少中"
else:
    delta_text = "急増中"
st.sidebar.metric(label="現在、周辺で待機中のファン推計",value=f"{waiting_fans:,}人", delta=delta_text)
if current_time <= 13:
    # 11時〜13時：ドーム周辺のカフェが激混み、少し離れたイオンは空いている
    cafe_data.loc[cafe_data['店名'] == 'カフェ乃木（仮）', '混雑度'] = '満席'
    cafe_data.loc[cafe_data['店名'] == 'カフェ乃木（仮）', '色'] = 'darkpurple'
    
    cafe_data.loc[cafe_data['店名'] == 'イオンモールナゴヤドーム前', '混雑度'] = '空席あり'
    cafe_data.loc[cafe_data['店名'] == 'イオンモールナゴヤドーム前', '色'] = 'blue'

elif current_time >= 15:
    # 15時以降：ファンが涼みに移動してイオンが激混み、ドーム周辺は空き始める
    cafe_data.loc[cafe_data['店名'] == 'カフェ乃木（仮）', '混雑度'] = '空席あり'
    cafe_data.loc[cafe_data['店名'] == 'カフェ乃木（仮）', '色'] = 'blue'
    
    cafe_data.loc[cafe_data['店名'] == 'イオンモールナゴヤドーム前', '混雑度'] = '満席'
    cafe_data.loc[cafe_data['店名'] == 'イオンモールナゴヤドーム前', '色'] = 'darkpurple'

col1, col2 = st.columns([2,1])
with col1:
    st.subheader("周辺の混雑・回遊マップ")
    m = folium.Map(location=[35.1895,136.9474], zoom_start=14)
    for i, row in cafe_data.iterrows():
        tooltip_html = f"""
            <b>{row['店名']}</b><br>
            状況: {row['混雑度']}<br>
            設備: {row['コラボ']}
        """

        folium.Marker(
            location=[row['緯度'], row['経度']],
            tooltip=tooltip_html,
            icon=folium.Icon(color=row['色'], icon='info-sign')
    ).add_to(m)

    st_folium(m, width=700, height=500, returned_objects=[])

with col2:
    st.subheader("おすすめ回遊ルート")

    empty_cafes = cafe_data[cafe_data['混雑度'] == '空席あり']

    if not empty_cafes.empty:
        recommended = empty_cafes.iloc[0]
        st.success(f"おすすめスポット: {recommended['店名']}\n\n現在空席あり。ここで#〇〇市で推し活 と投稿してイオン1000円クーポンGET！")
    else:
        st.warning("現在空席のあるカフェはありません。少し時間を空けるか、イオンモール等の大型待機所へご移動ください。")

    st.write("店舗リスト")
    st.dataframe(cafe_data[['店名', '混雑度', 'コラボ']])