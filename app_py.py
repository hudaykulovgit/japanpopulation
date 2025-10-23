# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import pandas as pd
# import numpy as np
# import requests
# import pydeck as pdk
# 
# st.set_page_config(page_title="Japan Population Density", page_icon="🗾", layout="wide")
# st.title("🗾 Japan Population Density Map")
# st.caption("Prefecture-level population density (people/km²). Source: Statistics Bureau of Japan (2023).")
# 
# # ---------------- Sidebar ----------------
# scheme = st.sidebar.selectbox("Color Scale", ["Quantiles", "Equal intervals"], index=0)
# k_bins = st.sidebar.slider("Color bins", 5, 9, 7)
# reverse = st.sidebar.checkbox("Reverse Colors", value=False)
# 
# # ---------------- Data ----------------
# data = {
#     "prefecture": [
#         "Hokkaido","Aomori","Iwate","Miyagi","Akita","Yamagata","Fukushima",
#         "Ibaraki","Tochigi","Gunma","Saitama","Chiba","Tokyo","Kanagawa",
#         "Niigata","Toyama","Ishikawa","Fukui","Yamanashi","Nagano","Gifu",
#         "Shizuoka","Aichi","Mie","Shiga","Kyoto","Osaka","Hyogo","Nara",
#         "Wakayama","Tottori","Shimane","Okayama","Hiroshima","Yamaguchi",
#         "Tokushima","Kagawa","Ehime","Kochi","Fukuoka","Saga","Nagasaki",
#         "Kumamoto","Oita","Miyazaki","Kagoshima","Okinawa"
#     ],
#     "population":[
#         5200000,1200000,1200000,2300000,950000,1060000,1800000,
#         2900000,1900000,1900000,7300000,6300000,14000000,9200000,
#         2200000,1040000,1150000,780000,810000,2050000,2000000,
#         3700000,7500000,1800000,1400000,2600000,8800000,5400000,
#         1300000,900000,550000,650000,1900000,2800000,1300000,
#         720000,950000,1300000,700000,5100000,800000,1300000,
#         1750000,1100000,1050000,1600000,1500000
#     ],
#     "area_km2":[
#         83450,9646,15278,7282,11613,9323,13784,
#         6097,6408,6362,3798,5158,2191,2416,
#         12584,4248,4186,4190,4465,13562,10621,
#         7777,5172,5777,4017,4612,1905,8396,
#         3691,4726,3507,6708,7114,8479,6112,
#         4146,1877,5676,7104,4986,2441,4105,
#         7409,6340,7735,9187,2276
#     ]
# }
# df = pd.DataFrame(data)
# df["density"] = df["population"] / df["area_km2"]
# 
# # English–Japanese prefecture map for joining
# name_map = {
#     "Hokkaido": "北海道","Aomori": "青森県","Iwate": "岩手県","Miyagi": "宮城県","Akita": "秋田県",
#     "Yamagata": "山形県","Fukushima": "福島県","Ibaraki": "茨城県","Tochigi": "栃木県","Gunma": "群馬県",
#     "Saitama": "埼玉県","Chiba": "千葉県","Tokyo": "東京都","Kanagawa": "神奈川県","Niigata": "新潟県",
#     "Toyama": "富山県","Ishikawa": "石川県","Fukui": "福井県","Yamanashi": "山梨県","Nagano": "長野県",
#     "Gifu": "岐阜県","Shizuoka": "静岡県","Aichi": "愛知県","Mie": "三重県","Shiga": "滋賀県",
#     "Kyoto": "京都府","Osaka": "大阪府","Hyogo": "兵庫県","Nara": "奈良県","Wakayama": "和歌山県",
#     "Tottori": "鳥取県","Shimane": "島根県","Okayama": "岡山県","Hiroshima": "広島県","Yamaguchi": "山口県",
#     "Tokushima": "徳島県","Kagawa": "香川県","Ehime": "愛媛県","Kochi": "高知県","Fukuoka": "福岡県",
#     "Saga": "佐賀県","Nagasaki": "長崎県","Kumamoto": "熊本県","Oita": "大分県","Miyazaki": "宮崎県",
#     "Kagoshima": "鹿児島県","Okinawa": "沖縄県"
# }
# df["pref_ja"] = df["prefecture"].map(name_map)
# 
# # ---------------- GeoJSON ----------------
# url = "https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson"
# geo = requests.get(url, timeout=30).json()
# 
# # Join data by Japanese name field
# pref_map = {row["pref_ja"]: row for row in df.to_dict("records")}
# for f in geo["features"]:
#     name_ja = f["properties"].get("nam_ja")
#     rec = pref_map.get(name_ja)
#     if rec:
#         f["properties"].update(rec)
#     else:
#         f["properties"]["density"] = None
# 
# # ---------------- Color bins ----------------
# vals = df["density"].dropna().values
# if scheme == "Quantiles":
#     bins = np.quantile(vals, np.linspace(0, 1, k_bins + 1))
# else:
#     bins = np.linspace(vals.min(), vals.max(), k_bins + 1)
# 
# base_colors = [
#     [237,248,233],[199,233,192],[161,217,155],
#     [116,196,118],[65,171,93],[35,139,69],
#     [0,109,44],[0,90,50],[0,68,27]
# ]
# palette = base_colors[:k_bins]
# if reverse: palette = list(reversed(palette))
# 
# def color_for_density(d):
#     if d is None or np.isnan(d): return [200,200,200,50]
#     idx = np.searchsorted(bins, d, side="right") - 1
#     idx = max(0, min(idx, len(palette)-1))
#     return palette[idx] + [180]
# 
# for f in geo["features"]:
#     d = f["properties"].get("density")
#     f["properties"]["fillColor"] = color_for_density(d)
# 
# # ---------------- Map ----------------
# layer = pdk.Layer(
#     "GeoJsonLayer",
#     geo,
#     pickable=True,
#     stroked=True,
#     filled=True,
#     get_fill_color="properties.fillColor",
#     get_line_color=[80,80,80],
#     lineWidthMinPixels=1,
# )
# view = pdk.ViewState(latitude=36.5, longitude=138.2, zoom=4.6)
# deck = pdk.Deck(
#     layers=[layer],
#     initial_view_state=view,
#     map_style="mapbox://styles/mapbox/light-v9",
#     tooltip={
#         "html": "<b>{prefecture}</b><br/>Population: {population:,}<br/>Area: {area_km2:,} km²<br/>Density: <b>{density:,.0f}</b> /km²",
#         "style": {"backgroundColor":"white","color":"black"}
#     },
# )
# st.pydeck_chart(deck, use_container_width=True)
# 
# # ---------------- Legend ----------------
# def legend_html():
#     html = ""
#     for i in range(len(palette)):
#         lo, hi = bins[i], bins[i+1]
#         r,g,b = palette[i]
#         html += (
#             f"<div style='display:flex;align-items:center;margin:2px 0'>"
#             f"<div style='width:20px;height:12px;background:rgb({r},{g},{b});border:1px solid #444;margin-right:6px'></div>"
#             f"{lo:,.0f} – {hi:,.0f}</div>"
#         )
#     return f"<div style='font-size:13px'>{html}</div>"
# 
# st.markdown("**Legend (people per km²)**")
# st.markdown(legend_html(), unsafe_allow_html=True)
# 
# # ---------------- Data Table ----------------
# st.dataframe(df.sort_values("density", ascending=False), use_container_width=True)
