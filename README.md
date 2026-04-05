# Live-Wait-Compass
地域回遊と混雑分散を促すダッシュボードのプロトタイプです。

##企画書(プロジェクトの背景・ロジック)
本システムの課題設定、インセンティブ設計などの詳細なプロセスについては、以下のNotionをご覧ください
https://www.notion.so/Live-Wait-Compass-33933166e170809cb7f8eb5d2f873ce0?source=copy_link

##使用技術
*Python 3.x(※開発・動作確認:Python 3.13.5)
*Streamlit(フロントエンド・UI)
*Pandas(データ処理)
*Folium/streamlit-folium(マッピング)

##ローカルでの実行方法
必要なライブラリをインストール後、以下のコマンドで起動します。
```bash
pip install streamlit pandas folium streamlit-folium geopy
streamlit run app.py
